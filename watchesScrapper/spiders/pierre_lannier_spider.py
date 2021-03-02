import scrapy
from watchesScrapper.src.logger import Logger
from watchesScrapper.src.utils import generate_default_dict
from HTMLTableToData import HTMLTableToData

class PierreLannierSpider(scrapy.Spider):
    name = 'pl'

    def start_requests(self):
        urls = [
            'https://www.pierre-lannier.fr/montres-homme.html?limit=all',
            'https://www.pierre-lannier.fr/montres-femme.html?limit=all'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        grid = response.css('ul.products-grid')
        items = grid.css('li')

        for item in items:
            infos = generate_default_dict('Pierre Lannier')
            link = response.urljoin(item.css('a::attr(href)').get())

            infos['url'] = link

            yield scrapy.Request(
                link, callback=self.parse_detail, meta={'item': infos}
            )

    def parse_detail(self, response):
        infos = response.meta['item']
        tables = response.css('#collapse-1 .panel-body table')
        materials = HTMLTableToData(tables[0].get()).to_json()
        characteristics = HTMLTableToData(tables[1].get()).to_json()
        glass_type = materials['type_de_verre'] if materials['type_de_verre'] else characteristics['type_de_verre']
        reference = response.css('#cont-product-name .sku::text').get()
        gender = self.get_gender(
            response.css('#cont-product-name .name::text').get()
        )
        images = response.css('.product-image-gallery img::attr(src)').getall()
        price = self.to_int(
            response.css('.price-box .price::text').get()
        )

        infos['glass'] = glass_type
        infos['case_form'] = materials['forme_du_boitier'][0]
        infos['diameter'] = self.to_int(materials['diametre_du_boitier'][0])
        infos['reference'] = reference
        infos['case_materials'] = materials['matiere_du_boitier']
        infos['strap_materials'] = materials['matiere_du_bracelet']
        infos['functions'] = characteristics['fonctions'][0].split('/')
        infos['movement'] = characteristics['collection'][0]
        infos['gender'] = gender
        infos['image_url'] = images
        infos['name'] = 'Pierre Lannier'
        infos['price'] = price
        infos['dial_colors'] = [materials['coloris_du_cadran'][0]]
        infos['strap_colors'] = [materials['coloris_du_bracelet'][0]]
        infos['bezel_colors'] = [materials['coloris_de_la_lunette'][0]]

        yield infos

    def to_int(self, diameter):
        return int(diameter.split(',')[0])

    def get_gender(self, title: str):
        if title.find('Homme') != -1:
            return 'Homme'
        elif title.find('Femme') != -1:
            return 'Femme'
        return 'Unisex'
