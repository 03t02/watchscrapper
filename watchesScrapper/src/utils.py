def generate_default_dict(brand: str, case_form='Round', movement='Automatic') -> dict:
    return {
        'brand': brand,
        'name': '',
        'reference': '',
        'price': 0,
        'gender': '',
        'image_url': [],
        'movement': movement,
        'diameter': 0,
        'case_form': case_form,
        'case_materials': [],
        'strap_materials': [],
        'functions': [],
        'glass': '',
        'url': '',
        'dial_colors': [],
        'strap_colors': [],
        'bezel_colors': []
    }


def price_to_int(string: str) -> int:
    return int(string.replace(',', ''), 10)
