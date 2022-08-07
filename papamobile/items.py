# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Car(scrapy.Item):
    url = scrapy.Field()
    time_date = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    
    brand = scrapy.Field()
    model = scrapy.Field()
    year_of_prod = scrapy.Field()
    displacement = scrapy.Field()
    fuel = scrapy.Field()
    power = scrapy.Field()
    gearbox = scrapy.Field()
    drive = scrapy.Field()
    chassis = scrapy.Field()
    color = scrapy.Field()
    import_country = scrapy.Field()
