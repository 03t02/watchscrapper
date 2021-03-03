import json_lines
import mysql.connector
from mysql.connector import errorcode
from utils import query_builder


try:
    cnx = mysql.connector.connect(
        user='root',
        password='416a922DM!',
        database='watch_engine',
        host='127.0.0.1'
    )
    with open('./seiko.jl', 'rb') as file:
        obj = {'brand': 'Seiko', 'reference': 'SNR029J1', 'price': 6000, 'gender': 'Male', 'movement': 'Automatic', 'diameter': 44, 'name': 'Prospex', 'power': 72, 'thickness': 15, 'caliber': '5r65', 'weight': '', 'image_urls': ['https://storage.seikowatches.com/image/2020/11/19044753143575/0/SNR029J1.png', 'https://storage.seikowatches.com/image/2020/11/19044753143575/0/SNR029J1.png'], 'case_form': 'Round', 'case_material': 'Titanium', 'strap_material': '', 'functions': ['Hours & Minutes', 'Date', 'Power reserve display'], 'glass': 'Saphir', 'url': 'https://www.seikowatches.com/fr-fr/products/prospex/snr029j1', 'dial_color': '', 'strap_color': '', 'bezel_color': '', 'water_proofing': 10}
        image_urls: list = obj.pop('image_urls', [])

        print(query_builder('watches', obj))
        cursor = cnx.cursor()
        cursor.execute(query_builder('watches', obj), obj)
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
