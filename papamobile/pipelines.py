# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_dynamodb import DynamoDbPipeline


# CSV Pipeline
# class PapamobilePipeline:
#     def process_item(self, item, spider):
#         with open("data.csv", "a") as f:
#             f.write(f'{item["time_date"]};{item["url"]};{item["title"]};{item["price"]}\n')


