import scrapy

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
        