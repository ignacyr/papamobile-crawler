import scrapy
from datetime import datetime


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    def start_requests(self):
        urls = [
            f'https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page={i}'
            for i in range(1, 2)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//a/@href').getall():
            if 'https://www.otomoto.pl/oferta/' in url:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_cars)

    def parse_cars(self, response):
        time_date = response.xpath('//span[@class="offer-meta__value"]/text()').get()
        months_map = {"stycznia": "01", "lutego": "02", "marca": "03",
                      "kwietnia": "04", "maja": "05", "czerwca": "06",
                      "lipca": "07", "sierpnia": "08", "września": "09",
                      "października": "10", "listopada": "11", "grudnia": "12"}
        for month in months_map.keys():
            time_date = time_date.replace(month, months_map[month])
        time_date = datetime.strptime(time_date, '%H:%M, %d %m %Y')

        title = response.xpath('//h1[@class="offer-title big-text"]/text()').getall()[-1].strip()
        title = ' '.join(title.split())

        print(title, time_date)
