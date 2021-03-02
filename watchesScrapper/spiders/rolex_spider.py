import scrapy
import time

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from watchesScrapper.src.utils import generate_default_dict

rolex_materials_dict = {
    'or everose': 'Or rose',
    'or jaune': 'Or jaune',
    'or gris': 'Or gris',
    'acier oystersteel': 'Acier inoxydable',
    'diamants': 'Diamants',
    'oysterflex': 'Caoutchouc',
    'platine': 'Platine',
    'caoutchouc': 'Caoutchouc',
    'second fuseau horaire': 'Double fuseau horaire',
    'jour et date': 'Jour et date',
    'date instantanée': 'Date',
    'chronographe': 'Chronographe',
    'heures, minutes': 'Heures, minutes',
    'phases de lune': 'Phase lunaire'
}


class RolexSpider(scrapy.Spider):
    name = 'rolex'

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=options
        )

    def start_requests(self):
        urls = [
            'https://www.rolex.com/fr/watches/datejust/all-models.html#p=1&f=+facet_gender:woman',
            # 'https://www.rolex.com/fr/watches/oyster-perpetual/all-models.html#p=1&f=+facet_gender:woman',
            # 'https://www.rolex.com/fr/watches/lady-datejust/all-models.html#p=1'
            # 'https://www.rolex.com/fr/watches/sky-dweller/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/submariner/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/datejust/all-models.html#p=1&f=+facet_gender:man',
            # 'https://www.rolex.com/fr/watches/oyster-perpetual/all-models.html#p=1&f=+facet_gender:man',
            # 'https://www.rolex.com/fr/watches/gmt-master-ii/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/day-date/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/cosmograph-daytona/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/sea-dweller/all-models.html#p=1',
            # 'https://www.rolex.com/fr/watches/cellini/all-models.html#p=1'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        navigation = response.css('ul[role="navigation"]')
        items = navigation[0].css('li')

        for item in items:
            infos = generate_default_dict(brand='Rolex')

            name = item.css('h2::text').get()
            caracteristics = item.css('figcaption span::text').get()
            diameter = self.get_diameter(caracteristics)
            materials = self.get_case_materials(caracteristics)

            infos['image_url'] = self.get_image_srcs(item)
            infos['name'] = name
            infos['diameter'] = diameter
            infos['case_materials'] = materials

            detail_link = item.css('a::attr(href)').get()
            detail_page = response.urljoin('/fr' + detail_link)
            yield scrapy.Request(detail_page, callback=self.parse_detail, meta={'item': infos})

    def parse_detail(self, response):
        self.driver.get(response.url)

        try:
            button = self.driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
            button.click()
            time.sleep(2)
        except NoSuchElementException:
            print('No cookies found')

        infos = response.meta['item']
        region = response.css('div[role="region"]')[0]
        infos['reference'] = self.get_reference(region)

        if self.page_has_loaded():
            selenium_response = Selector(text=self.driver.page_source)
            price = selenium_response.css('.sc-fzoXzr.sc-fznWqX.sc-qOubn.kbgcwh span::text').get()
            if price is not None and price.find('€') != -1:
                infos['price'] = int(''.join(price.split(' ')[0:2]))
            else:
                infos['price'] = 0

        bracelet_material = region.css('li')[2].css('dl').css('dd::text')[1].get().strip()
        function = region.css('li')[1].css('dl').css('dd::text')[3].get().strip()

        infos['functions'] = self.get_function(function)
        infos['strap_materials'] = self.define_bracelet_material(bracelet_material)
        yield infos

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def get_reference(self, region):
        return region.css('ul')[0].css('span::text').get().split(' ')[1]

    def define_bracelet_material(self, text):
        tmp_text = text.lower()

        if tmp_text == 'flexibles':
            return 'caoutchouc'
        elif tmp_text.find('or jaune') != -1:
            return 'or jaune'
        elif tmp_text.find('or everose') != -1:
            return 'or everose'
        return 'acier oystersteel'

    def get_case_materials(self, caracteristics):
        tmp_materials = caracteristics.split(',')[1:3][1]
        tmp_materials = tmp_materials.split('et')
        materials = []

        for tmp_material in tmp_materials:
            materials.append(tmp_material.lower().strip())
        return materials

    def get_diameter(self, caracteristics: str) -> int:
        diameter = caracteristics.split(',')[1:3][0]
        return int(diameter.replace(u'\xa0', u'').strip()[0:2])

    def get_image_srcs(self, item) -> str:
        img_srcset = item.css('picture source::attr(srcset)')
        return img_srcset[2].get().split(',')[1].strip().split(' ')[0]

    def get_function(self, selector):
        functions = ['heures et minutes']

        for function in selector.split('.'):
            tmp = function.lower()
            if tmp.find('chronographe') != -1:
                functions.append('chronographe')
            elif tmp.find('phases de lune') != -1:
                functions.append('phases de lune')
            elif tmp.find('second fuseau horaire') != -1:
                functions.append('second fuseau horaire')
            elif tmp.find('jour et date') != -1:
                functions.append('jour et date')
            elif tmp.find('date instantanée') != -1:
                functions.append('date')
        return functions
