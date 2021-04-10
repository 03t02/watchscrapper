from logger import Logger


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


def no_utf8(string: str) -> str:
    translation = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")
    return string.translate(translation)


def format_key(key: str) -> str:
    return no_utf8(key.replace(' ', '_')).lower() or 'default_key'


def get_int(string: str) -> int:
    chunks: list = string.split(' ')
    for chunk in chunks:
        if chunk.isdigit():
            return int(chunk)
    return 0


def get_dict_keys(obj: dict) -> list[str]:
    return list(obj.keys())


def snake_case_to_camel_case(string: str) -> str:
    arr_str: list[str] = list(string)

    for idx, new_str in enumerate(arr_str):
        if new_str == '_':
            arr_str[idx + 1] = arr_str[idx + 1].capitalize()
            del arr_str[idx]
    return ''.join(arr_str)


def list_key_camel_case(array: list[str]) -> list[str]:
    new_arr: list[str] = []

    for arr in array:
        new_arr.append(snake_case_to_camel_case(arr))
    return new_arr


def dict_key_camel_case(obj: dict) -> dict:
    new_dict: dict = {}

    for key in list(obj.keys()):
        new_key = snake_case_to_camel_case(key)
        new_dict[new_key] = obj[key]
    return new_dict


def insert_into_builder(table_name: str, keys: list[str]) -> str:
    return 'INSERT INTO ' + table_name + '(' + ','.join(keys) + ')'


def values_builder(keys: list[str]) -> str:
    new_arr: list[str] = []

    for key in keys:
        new_arr.append('%({})s'.format(key))
    return 'VALUES(' + ','.join(new_arr) + ')'


def query_builder(table_name: str, obj: dict):
    """
    INSERT INTO watches(keys)
    VALUES(keys)
    """
    keys: list[str] = list_key_camel_case(get_dict_keys(obj))
    query = """{} {}""".format(insert_into_builder(table_name, keys), values_builder(keys))
    return query
