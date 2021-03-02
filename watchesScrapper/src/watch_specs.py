from watchesScrapper.src.logger import Logger


class WatchSpecs:
    __brand: str = None
    __reference: str = None
    __price: int = None
    __gender: str = None
    __movement: str = 'Automatic'
    __diameter: int = 0
    __name: str = None
    __case_form: str = 'Round'
    __glass: str = None
    __url: str = None
    __image_urls: list = []
    __case_materials: list = []
    __strap_materials: list = []
    __functions: list = []
    __dial_colors: list = []
    __strap_colors: list = []
    __bezel_colors: list = []

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
    def case_materials(self):
        return self.__case_materials

    @property
    def strap_materials(self):
        return self.__strap_materials

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
    def dial_colors(self):
        return self.__dial_colors

    @property
    def strap_colors(self):
        return self.__strap_colors

    @property
    def bezel_colors(self):
        return self.__bezel_colors

    @brand.setter
    def brand(self, brand: str):
        if type(brand) is str:
            self.__brand = brand
        else:
            Logger.warn('brand property should be an str type.')

    @strap_colors.setter
    def strap_colors(self, strap_colors: list):
        if type(strap_colors) is list:
            self.__strap_colors = strap_colors
        else:
            Logger.warn('strap_colors property should be a list type.')

    @bezel_colors.setter
    def bezel_colors(self, bezel_colors: list):
        if type(bezel_colors) is list:
            self.__bezel_colors = bezel_colors
        else:
            Logger.warn('bezel_colors property should be a list type.')

    @dial_colors.setter
    def dial_colors(self, dial_colors: list):
        if type(dial_colors) is list:
            self.__dial_colors = dial_colors
        else:
            Logger.warn('dial_colors property should be a list type.')

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

    @strap_materials.setter
    def strap_materials(self, strap_materials: list):
        if type(strap_materials) is list:
            self.__strap_materials = strap_materials
        else:
            Logger.warn('strap_materials property should be a list type.')

    @case_materials.setter
    def case_materials(self, case_materials: list):
        if type(case_materials) is list:
            self.__case_materials = case_materials
        else:
            Logger.warn('case_materials property should be a list type.')

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
            'image_urls': self.image_urls,
            'case_form': self.case_form,
            'case_materials': self.case_materials,
            'strap_materials': self.strap_materials,
            'functions': self.functions,
            'glass': self.glass,
            'url': self.url,
            'dial_colors': self.dial_colors,
            'strap_colors': self.strap_colors,
            'bezel_colors': self.bezel_colors
        }
