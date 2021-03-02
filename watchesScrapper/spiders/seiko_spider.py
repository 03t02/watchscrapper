import scrapy
from watchesScrapper.src.logger import Logger
from watchesScrapper.src.utils import generate_default_dict, price_to_int
from watchesScrapper.src.watch_specs import WatchSpecs
from watchesScrapper.src.constant import HOURS_MINUTES, DATE, DAY, DAY_DATE, \
    ALARM, CHRONOGRAPH, SECOND_TIMEZONE, AUTOMATIC, SOLAR


class SeikoSpider(scrapy.Spider):
    name = 'seiko'

    def start_requests(self):
        urls = [
            'https://www.seikowatches.com/fr-fr/products/lukia/lineup',
            'https://www.seikowatches.com/fr-fr/products/prospex/lineup',
            'https://www.seikowatches.com/fr-fr/products/presage/lineup',
            'https://www.seikowatches.com/fr-fr/products/5sports/lineup'
        ]

        Logger.info('Seiko spider')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('.lu-List_Item')

        for item in items:
            infos = WatchSpecs()

            name = item.css('.lu-List_Collection::text').get()
            reference = item.css('.lu-List_Name::text').get()
            price = item.css('.lu-List_PriceTaxIn span')[1].css('::text').get()
            gender = item.css('.lu-List_Target div::text').get()
            link = response.urljoin(item.css('a::attr(href)').get())

            infos.brand = 'Seiko'
            infos.name = name
            infos.reference = reference
            infos.price = price_to_int(price)
            infos.gender = gender
            infos.url = link

            yield scrapy.Request(link, callback=self.parse_detail, meta={'item': infos})

    def parse_detail(self, response):
        infos = response.meta['item']
        image = response.css('.okra-carousel-slide-inner img::attr(src)').get()
        spec_groups = response.css('.pr-Spec_Group')
        movement = spec_groups[0]
        materials = spec_groups[1]
        diameter = spec_groups[2]
        function = spec_groups[3]
        case_materials = self.get_case_materials(materials)
        glass = response.css('#innerExterior > div:nth-child(2) > div > p::text').get()

        infos.image_urls = image if type(image) is list else [image]
        infos.movement = self.get_movement(movement)
        infos.diameter = int(self.get_diameter(diameter).split('.')[0])
        infos.case_materials = case_materials
        infos.glass = glass

        strap_materials = self.get_strap_materials(materials)
        if strap_materials is not None:
            infos.strap_materials = [strap_materials]
        else:
            infos.strap_materials = case_materials
        infos.functions = self.get_function(function)
        yield infos.to_json()

    def get_movement(self, selector):
        tmp = selector.css('#innerMovement').css('.pr-Spec_Item')[1].css('p::text').get().lower()

        if tmp.find('spring drive') != -1:
            return AUTOMATIC
        elif tmp.find('solaire') != -1:
            return SOLAR
        return AUTOMATIC

    def get_diameter(self, selector):
        return selector.css('.pr-Spec_Item').css('.pr-Spec_Text div::text').getall()[1]

    def get_case_materials(self, selector):
        str_arr = selector.css('*::text').getall()[2].split(' et ')
        materials = []

        if len(str_arr) == 2:
            materials.append(str_arr[0])
            materials.append(str_arr[1])
        else:
            materials.append(str_arr[0])
        return materials

    def get_strap_materials(self, selector):
        str_arr = selector.css('*::text').getall()

        for idx, val in enumerate(str_arr):
            if val.find('Matière du bracelet') != -1:
                return str_arr[idx + 1]
        return None

    def get_function(self, selector):
        tmp = selector.css('*::text').getall()
        functions = [HOURS_MINUTES]

        for item in tmp[1:len(tmp)]:
            string = item.lower()
            if string.find('à double fuseau') != -1:
                functions.append(SECOND_TIMEZONE)
            elif string.find('alarme') != -1:
                functions.append(ALARM)
            elif string.find('chronographe') != -1:
                functions.append(CHRONOGRAPH)
            elif string.find('affichage du jour et de la date') != -1:
                functions.append(DAY_DATE)
            elif string.find('affichage de la date') != -1:
                functions.append(DATE)
        return functions
