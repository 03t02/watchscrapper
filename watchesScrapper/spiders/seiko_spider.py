import scrapy
from watchesScrapper.src.logger import Logger
from watchesScrapper.src.utils import generate_default_dict, price_to_int \
    ,format_key, get_int
from watchesScrapper.src.watch_specs import WatchSpecs
from watchesScrapper.src.constant import HOURS_MINUTES, DATE, DAY, DAY_DATE \
    ,ALARM, CHRONOGRAPH, SECOND_TIMEZONE, AUTOMATIC, SOLAR, MALE, FEMALE \
    ,SAPHIR, STAINLESS_STEEL, HARDLEX, CORDOVAN_LEATHER, CROCODILE_LEATHER\
    ,POWER_RESERVE, TITANIUM


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
            infos.gender = self.translate_gender(gender)
            infos.url = link

            yield scrapy.Request(link, callback=self.parse_detail, meta={'item': infos})

    def parse_detail(self, response):
        infos = response.meta['item']
        image = response.css('.okra-carousel-slide-inner img::attr(src)').get()
        spec_groups = response.css('.pr-Spec_Group')

        movement = self.spec_group_to_dict(spec_groups[0])
        materials = self.spec_group_to_dict(spec_groups[1])
        size = spec_groups[2].css('.pr-Spec_Item :not(h4)::text').getall()
        function = spec_groups[3]

        infos.image_urls = image if type(image) is list else [image]
        infos.movement = self.get_movement(movement['type_de_mouvement'])
        infos.caliber = movement['numero_du_calibre']
        infos.power = self.get_power(movement)
        infos.case_material = self.translate_materials(materials['composition_du_boitier'])\
            if 'composition_du_boitier' in materials else ''
        infos.glass = self.get_glass(materials['composition_du_verre'])
        infos.strap_material = self.translate_materials(materials['matiere_du_bracelet'])\
            if 'matiere_du_bracelet' in materials else ''
        infos.functions = self.get_function(function)
        infos.diameter = self.get_diameter(size)
        infos.thickness = self.get_thickness(size)

        yield infos.to_json()

    def spec_group_to_dict(self, group, selector='p::text'):
        dict = {}
        spec_items = group.css('.pr-Spec_Item')

        for item in spec_items:
            key = format_key(item.css('h4::text').get())
            value = item.css('p::text').get().lower()
            dict[key] = value
        return dict

    def get_power(self, movement) -> int:
        if 'autonomie' in movement:
            Logger.warn('Power: ' + str(get_int(movement['autonomie'])))
            return get_int(movement['autonomie'])
        return 0

    def translate_gender(self, gender: str):
        if gender == 'Homme':
            return MALE
        return FEMALE

    def get_glass(self, glass: str):
        if glass.lower().find('hardlex') != -1:
            return HARDLEX
        return SAPHIR

    def translate_materials(self, material: str):
        lowercase_material = material.lower()
        if lowercase_material.find('acier inoxydable') != -1:
            return STAINLESS_STEEL
        elif lowercase_material.find('cuir cordovan') != -1:
            return CORDOVAN_LEATHER
        elif lowercase_material.find('cuir de crocodile') != -1:
            return CROCODILE_LEATHER
        elif lowercase_material.find('titane') != -1:
            return TITANIUM
        return STAINLESS_STEEL

    def get_movement(self, movement_type: str):
        if movement_type.find('spring drive') != -1:
            return AUTOMATIC
        elif movement_type.find('solaire') != -1:
            return SOLAR
        return AUTOMATIC

    def get_diameter(self, values: list):
        for i in range(len(values)):
            if values[i].find('Diamètre') != -1:
                return int(values[i + 1].split('.')[0])
        return 0

    def get_thickness(self, values: list):
        for i in range(len(values)):
            if values[i].find('Épaisseur') != -1:
                return int(values[i + 1].split('.')[0])
        return 0

    def get_function(self, selector):
        tmp = selector.css(':not(h3)::text').getall()
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
            elif string.find('affichage de la réserve de marche') != -1:
                functions.append(POWER_RESERVE)
        return functions
