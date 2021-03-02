import scrapy

from math import ceil, floor
from datetime import date
from watchesScrapper.src.logger import Logger


class Chrono24Spider(scrapy.Spider):
    name = 'chrono24'

    def start_requests(self):
        for url in self.start_urls:
            fields = url['fields']
            Logger.info('url ' + fields['chrono24Link'])
            yield scrapy.Request(
                url=fields['chrono24Link'] + '&pageSize=120&SETLANG=fr_FR&SETCURR=EUR',
                callback=self.parse,
                meta={
                    'meta': {
                        'brand': fields['brand'],
                        'reference': fields['reference'],
                        'name': fields['name'],
                        'id': url['id']
                    }
                }
            )

    def parse(self, response):
        meta_data = response.meta['meta']
        items = response.css('.article-item-container')
        nb_listing = response.css('.result-page-headline .text-center::text') \
            .get().strip().split(' ')[0]
        prices = []
        sum_price = 0

        Logger.info('Visiting URL ' + response.url)
        for item in items:
            price = item.css('.article-price strong::text').get().strip()
            if price != 'Prix sur demande':
                formatted_price = int(price.replace('.', ''))
                prices.append(formatted_price)

        prices.sort()
        zoned_prices = self.restrict_prices(prices)

        for price in zoned_prices:
            sum_price = sum_price + price
        average_price = ceil(sum_price / len(zoned_prices))
        median_price = zoned_prices[ceil(len(zoned_prices) / 2)]
        today = date.today().strftime('%d/%m/%y')

        Logger.success('Yielding item')
        yield {
            'brand': meta_data['brand'],
            'name': meta_data['name'],
            'reference': meta_data['reference'],
            'averagePrice': self.remove_commission(average_price),
            'medianPrice': self.remove_commission(median_price),
            'date': today,
            'nbListing': int(nb_listing),
            'priceTrendPrediction': self.compute_price_trending(zoned_prices),
            'watch_id': [meta_data['id']]
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
        q2 = floor(len(prices) / 2)
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

    def remove_commission(self, price):
        return price - (price * (6.5 / 100))
