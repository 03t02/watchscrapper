# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from airtable.airtable import Airtable
from watchesScrapper.src.constant import AIRTABLE_BASE_KEY, AIRTABLE_API_KEY
from watchesScrapper.src.logger import Logger


class WatchStockPipeline:
    watches_table = Airtable(
        AIRTABLE_BASE_KEY,
        'watches',
        AIRTABLE_API_KEY
    )
    prices_table = Airtable(
        AIRTABLE_BASE_KEY,
        'prices',
        AIRTABLE_API_KEY
    )

    def open_spider(self, spider):
        """
        In this method, we fetch urls from Airtable and assign them to start_urls.
        This list of urls are automatically used in the chrono24_spider

        :param spider:
        :return:
        """
        if spider.name == 'chrono24':
            at_results = self.watches_table.get_all()
            urls = []

            for result in at_results:
                if len(result):
                    urls.append(result)
            Logger.success(len(urls))
            spider.start_urls = urls

    def process_item(self, item, spider):
        if spider.name == 'chrono24':
            if 'watch_id' in item:
                self.prices_table.insert(item)
                Logger.success('Inserted item')
            else:
                Logger.success('Data are stored')
        return item
