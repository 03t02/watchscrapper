import json_lines
import mysql.connector
from mysql.connector import errorcode
from utils import query_builder, dict_key_camel_case
from logger import Logger


try:
    cnx = mysql.connector.connect(
        user='root',
        password='416a922DM!',
        database='watch_engine',
        host='127.0.0.1'
    )
    with open('./seiko.jl', 'rb') as file:
        obj = {
            'brand': 'Seiko',
            'reference': 'SNR029J1',
            'price': 6000,
            'gender': 'Male',
            'movement': 'Automatic',
            'diameter': 44,
            'name': 'Prospex',
            'power': 72,
            'thickness': 15,
            'caliber': '5r65',
            'weight': 0,
            'image_urls': [
                'https://storage.seikowatches.com/image/2020/11/19044753143575/0/SNR029J1.png',
                'https://storage.seikowatches.com/image/2020/11/19044753143575/0/SNR029J1.png'
            ],
            'case_form': 'Round',
            'case_material': 'Titanium',
            'strap_material': '',
            'functions': ['Hours & Minutes', 'Date', 'Power reserve display'],
            'glass': 'Saphir',
            'url': 'https://www.seikowatches.com/fr-fr/products/prospex/snr029j1',
            'dial_color': '',
            'strap_color': '',
            'bezel_color': '',
            'water_proofing': 10
        }
        image_urls: list = obj.pop('image_urls', [])
        functions: list = obj.pop('functions', [])

        cursor = cnx.cursor()
        cursor.execute(query_builder('watches', obj), dict_key_camel_case(obj))
        last_id = cursor.lastrowid

        for url in image_urls:
            image_url_query = (
                'INSERT INTO image_urls(url, watch_id)'
                'VALUES (%(url)s, %(watch_id)s)'
            )
            cursor.execute(image_url_query, {'url': url, 'watch_id': last_id})
        for function in functions:
            function_query = (
                'INSERT INTO functions(function, watch_id)'
                'VALUES (%(function)s, %(watch_id)s)'
            )
            cursor.execute(function_query, {'function': function, 'watch_id': last_id})
        cnx.commit()
        cursor.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
