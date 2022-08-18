# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_dynamodb import DynamoDbPipeline
import requests
import json


# CSV Pipeline
# class PapamobilePipeline:
#     def process_item(self, item, spider):
#         with open("data.csv", "a") as f:
#             f.write(f'{item["time_date"]};{item["url"]};{item["title"]};{item["price"]}\n')


class TranslateLangPipeline:
    def process_item(self, item, spider):
        trans_countries = {'Polska': 'Poland', 'Niemcy': 'Germany', 'Francja': 'France', 'Belgia': 'Belgium', 'Holandia': 'Netherlands',
                           'Szwajcaria': 'Switzerland', 'Włochy': 'Italy', 'Szwecja': 'Sweden', 'Luksemburg': 'Luxembourg', 
                           'Dania': 'Denmark', 'Hiszpania': 'Spain', 'Irlandia': 'Ireland', 'Kanada': 'Canada'}
        trans_colors = {'Biały': 'White', 'Szary': 'Gray', 'Czarny': 'Black', 'Czerwony': 'Red', 
                        'Srebrny': 'Silver', 'Niebieski': 'Blue', 'Żółty': 'Yellow', 'Zielony': 'Green',
                        'Złoty': 'Gold', 'Brązowy': 'Brown', 'Fioletowy': 'Purple', 'Inny kolor': 'Other',
                        'Bordowy': 'Red', 'Beżowy': 'Other'}
        trans_fuel = {'Benzyna': 'Petrol', 'Hybryda': 'Hybrid', 'Elektryczny': 'Electric'}

        for key in item.keys():
            if type(item[key]) is str:
                for country in trans_countries.keys():
                    item[key] = item[key].replace(country, trans_countries[country])
                for color in trans_colors.keys():
                    item[key] = item[key].replace(color, trans_colors[color])
                for fuel in trans_fuel.keys():
                    item[key] = item[key].replace(fuel, trans_fuel[fuel])

        return item


class RestApiPipeline:
    def process_item(self, item, spider):
        api_url = "http://34.141.144.103:8000/base/add"
        response = requests.post(api_url, json=dict(item))
        print(response.json())
        return item
