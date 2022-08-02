import scrapy


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    def start_requests(self):
        urls = [
            'https://nofluffjobs.com/pl'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'otomoto.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

