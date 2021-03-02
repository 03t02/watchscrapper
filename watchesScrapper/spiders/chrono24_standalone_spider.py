import scrapy

from math import ceil, floor
from datetime import date
from watchesScrapper.src.logger import Logger


class Chrono24StandaloneSpider(scrapy.Spider):
    name = 'chrono24_standalone'
    url = ''

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']

        super(Chrono24StandaloneSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.url + '&pageSize=120&SETLANG=fr_FR&SETCURR=EUR',
            callback=self.parse
        )

    def parse(self, response):
        items = response.css('.article-item-container')
        nb_listing = int(
            response.css('.result-page-headline .text-center::text') \
                .get().strip().split(' ')[0]
        )
        prices = []
        sum_price = 0

        Logger.info('Visiting URL ' + response.url)
        for item in items:
            price = item.css('.article-price strong::text').get().strip()
            if price != 'Prix sur demande':
                formatted_price = int(price.replace('.', ''))
                sum_price = sum_price + formatted_price
                prices.append(formatted_price)

        prices.sort()
        average_price = ceil(sum_price / len(prices))
        median_price = prices[ceil(len(prices) / 2)]
        today = date.today().strftime('%d/%m/%y')

        Logger.success('Yielding item')
        yield {
            'averagePrice': average_price,
            'medianPrice': median_price,
            'date': today,
            'nbListing': nb_listing,
            'priceTrendPrediction': self.compute_price_trending(
                self.restrict_prices(prices)
            )
        }

    def compute_price_trending(self, prices) -> int:
        lowest = prices[0]
        highest = prices[len(prices) - 1]
        half_price_diff = (highest - lowest) / 2
        middle_price = lowest + half_price_diff
        lower_prices = []
        higher_prices = []

        for price in prices:
            if price > middle_price:
                higher_prices.append(price)
            else:
                lower_prices.append(price)

        if len(lower_prices) > len(higher_prices):
            return 'DOWN'
        elif len(lower_prices) < len(higher_prices):
            return 'UP'
        return 'EQUAL'

    def get_outliers_limits(self, prices):
        fh = prices[0:floor(len(prices) / 2)]
        sh = prices[floor(len(prices) / 2):len(prices) - 1]
        q1 = floor(len(fh) / 2)
        q3 = floor(len(sh) / 2)

        outlowlim = prices[q1] / 1.5
        outhighlim = prices[q3] * 1.5

        return [outlowlim, outhighlim]

    def restrict_prices(self, prices):
        outliers = self.get_outliers_limits(prices)
        low = outliers[0]
        high = outliers[1]
        restricted_prices = []

        for price in prices:
            if price >= low and price <= high:
                restricted_prices.append(price)
        return restricted_prices
