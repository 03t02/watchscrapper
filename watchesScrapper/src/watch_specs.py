from watchesScrapper.src.logger import Logger


class WatchSpecs:
    __brand: str = ''
    __reference: str = ''
    __price: int = 0
    __gender: str = ''
    __movement: str = 'Automatic'
    __diameter: int = 0
    __name: str = ''
    __case_form: str = 'Round'
    __glass: str = ''
    __url: str = ''
    __power: int = 0
    __caliber: str = ''
    __weight: str = ''
    __thickness: int = 0
    __case_material: str = ''
    __strap_material: str = ''
    __dial_color: str = ''
    __strap_color: str = ''
    __bezel_color: str = ''
    __water_proofing_bars: int = 0
    __image_urls: list = []
    __functions: list = []

    @property
    def thickness(self):
        return self.__thickness

    @property
    def water_proofing_bars(self):
        return self.__water_proofing_bars

    @property
    def weight(self):
        return self.__weight

    @property
    def caliber(self):
        return self.__caliber

    @property
    def power(self):
        return self.__power

    @property
    def brand(self):
        return self.__brand

    @property
    def reference(self):
        return self.__reference

    @property
    def price(self):
        return self.__price

    @property
    def gender(self):
        return self.__gender

    @property
    def movement(self):
        return self.__movement

    @property
    def diameter(self):
        return self.__diameter

    @property
    def name(self):
        return self.__name

    @property
    def image_urls(self):
        return self.__image_urls

    @property
    def case_form(self):
        return self.__case_form

    @property
    def case_material(self):
        return self.__case_material

    @property
    def strap_material(self):
        return self.__strap_material

    @property
    def functions(self):
        return self.__functions

    @property
    def glass(self):
        return self.__glass

    @property
    def url(self):
        return self.__url

    @property
    def dial_color(self):
        return self.__dial_color

    @property
    def strap_color(self):
        return self.__strap_color

    @property
    def bezel_color(self):
        return self.__bezel_color

    @thickness.setter
    def thickness(self, thickness: int):
        if type(thickness) is int:
            self.__thickness = thickness
        else:
            Logger.warn('thickness property should be an int type.')

    @water_proofing_bars.setter
    def water_proofing_bars(self, water_proofing_bars: int):
        if type(water_proofing_bars) is int:
            self.__water_proofing_bars = water_proofing_bars
        else:
            Logger.warn('water_proofing_bars property should be an int type.')

    @weight.setter
    def weight(self, weight: int):
        if type(weight) is int:
            self.__weight = weight
        else:
            Logger.warn('weight property should be an int type.')

    @caliber.setter
    def caliber(self, caliber: str):
        if type(caliber) is str:
            self.__caliber = caliber
        else:
            Logger.warn('caliber property should be an str type.')

    @power.setter
    def power(self, power: int):
        if type(power) is int:
            self.__power = power
        else:
            Logger.warn('power property should be an int type')

    @brand.setter
    def brand(self, brand: str):
        if type(brand) is str:
            self.__brand = brand
        else:
            Logger.warn('brand property should be an str type.')

    @strap_color.setter
    def strap_color(self, strap_color: str):
        if type(strap_color) is str:
            self.__strap_color = strap_color
        else:
            Logger.warn('strap_color property should be a str type.')

    @bezel_color.setter
    def bezel_color(self, bezel_color: str):
        if type(bezel_color) is str:
            self.__bezel_color = bezel_color
        else:
            Logger.warn('bezel_color property should be an str type.')

    @dial_color.setter
    def dial_color(self, dial_color: str):
        if type(dial_color) is str:
            self.__dial_color = dial_color
        else:
            Logger.warn('dial_color property should be an str type.')

    @url.setter
    def url(self, url: str):
        if type(url) is str:
            self.__url = url
        else:
            Logger.warn('url property should be an str type.')

    @glass.setter
    def glass(self, glass: str):
        if type(glass) is str:
            self.__glass = glass
        else:
            Logger.warn('glass property should be an str type.')

    @functions.setter
    def functions(self, functions: list):
        if type(functions) is list:
            self.__functions = functions
        else:
            Logger.warn('functions property should be a list type.')

    @strap_material.setter
    def strap_material(self, strap_material: str):
        if type(strap_material) is str:
            self.__strap_material = strap_material
        else:
            Logger.warn('strap_material property should be an str type.')

    @case_material.setter
    def case_material(self, case_material: str):
        if type(case_material) is str:
            self.__case_material = case_material
        else:
            Logger.warn('case_material property should be an str type.')

    @case_form.setter
    def case_form(self, case_form: str):
        if type(case_form) is str:
            self.__case_form = case_form
        else:
            Logger.warn('case_form property should be an str type.')

    @image_urls.setter
    def image_urls(self, image_urls: list):
        if type(image_urls) is list:
            self.__image_urls = image_urls
        else:
            Logger.warn('image_urls property should be a list type.')

    @name.setter
    def name(self, name: str):
        if type(name) is str:
            self.__name = name
        else:
            Logger.warn('name property should be an str type.')

    @diameter.setter
    def diameter(self, diameter: int):
        if type(diameter) is int:
            self.__diameter = diameter
        else:
            Logger.warn('diameter property should be an int type.')

    @movement.setter
    def movement(self, movement: str):
        if type(movement) is str:
            self.__movement = movement
        else:
            Logger.warn('movement property should be an str type.')

    @gender.setter
    def gender(self, gender: str):
        if type(gender) is str:
            self.__gender = gender
        else:
            Logger.warn('gender property should be an str type.')

    @reference.setter
    def reference(self, reference: str):
        if type(reference) is str:
            self.__reference = reference
        else:
            Logger.warn('reference property should be an str type.')

    @price.setter
    def price(self, price: int):
        if type(price) is int:
            self.__price = price
        else:
            Logger.warn('price property should be an int type.')

    def to_json(self):
        return {
            'brand': self.brand,
            'reference': self.reference,
            'price': self.price,
            'gender': self.gender,
            'movement': self.movement,
            'diameter': self.diameter,
            'name': self.name,
            'power': self.power,
            'thickness': self.thickness,
            'caliber': self.caliber,
            'weight': self.weight,
            'image_urls': self.image_urls,
            'case_form': self.case_form,
            'case_material': self.case_material,
            'strap_material': self.strap_material,
            'functions': self.functions,
            'glass': self.glass,
            'url': self.url,
            'dial_color': self.dial_color,
            'strap_color': self.strap_color,
            'bezel_color': self.bezel_color
        }
