import scrapy
from datetime import datetime, timedelta
import lxml.html
from papamobile.items import Car

class OtomotoSpider(scrapy.Spider):
    name = "otomoto"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.break_after_old = 100
        self.yesterday = datetime.today().date() - timedelta(days=1)
        self.old_cars_counter = 0 

    def start_requests(self):
        urls = [
            f'https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page={i}'
            for i in range(1, 201)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//a/@href').getall():
            if 'https://www.otomoto.pl/oferta/' in url:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_cars)

    def parse_cars(self, response):
        car = Car()
        
        time_date = response.xpath('//span[@class="offer-meta__value"]/text()').get()
        months_map = {"stycznia": "01", "lutego": "02", "marca": "03",
                      "kwietnia": "04", "maja": "05", "czerwca": "06",
                      "lipca": "07", "sierpnia": "08", "września": "09",
                      "października": "10", "listopada": "11", "grudnia": "12"}
        for month in months_map.keys():
            time_date = time_date.replace(month, months_map[month])
        car["added"] = datetime.strptime(time_date, '%H:%M, %d %m %Y')
        
        if car["added"].date() == self.yesterday:
            title = response.xpath('//h1[@class="offer-title big-text"]/text()').getall()[-1].strip()
            car["title"] = ' '.join(title.split())
    
            price = response.xpath('//span[@class="offer-price__number"]/text()').get()
            car["price"] = int(''.join(filter(str.isdigit, price)))
    
            offer_params = response.xpath('//li[@class="offer-params__item"]').getall()
    
            par_keys = [lxml.html.fromstring(param).xpath('//span[@class="offer-params__label"]/text()')[0] for param in offer_params]
            par_values = [lxml.html.fromstring(param).xpath('//div[@class="offer-params__value"]/text()')[0].strip() for param in offer_params]
            par_values = [v for v in par_values if v]
    
            params = {lxml.html.fromstring(param).xpath('//span[@class="offer-params__label"]/text()')[0]:
                      lxml.html.fromstring(param).xpath('//div[@class="offer-params__value"]/text()')[0].strip()
                      if lxml.html.fromstring(param).xpath('//div[@class="offer-params__value"]/text()')[0].strip()
                      else lxml.html.fromstring(param).xpath('//div[@class="offer-params__value"]/a/text()')[0].strip()
                      for param in offer_params}
     
            features = [item.strip()
                        for item in response.xpath('//li[@class="parameter-feature-item"]/text()').getall()
                        if item.strip()]
                        
            cut_url = response.url[30:]
            car["url"] = cut_url
            
            car["added"] = car["added"].strftime("%Y-%m-%d")
            if params.get("Marka pojazdu"):
                car["brand"] = params["Marka pojazdu"]
            else:
                car["brand"] = "None"
            if params.get("Model pojazdu"):
                car["model"] = params["Model pojazdu"]
            else:
                car["model"] = "None"
            if params.get("Rok produkcji"):
                car["year"] = params["Rok produkcji"]
            else:
                car["year"] = 0
            if params.get("Pojemność skokowa"):
                car["displacment"] = int(''.join(filter(str.isdigit, params["Pojemność skokowa"]))[:-1])
            else:
                car["displacment"] = 0
            if params.get("Rodzaj paliwa"):
                car["fuel"] = params["Rodzaj paliwa"]
            else:
                car["fuel"] = "None"
            if params.get("Moc"):
                car["power"] = int(''.join(filter(str.isdigit, params["Moc"])))
            else:
                car["power"] = 0
            if params.get("Skrzynia biegów"):
                car["gearbox"] = params["Skrzynia biegów"]
            else:
                car["gearbox"] = "None"
            if params.get("Napęd"):
                car["drive"] = params["Napęd"]
            else:
                car["drive"] = "None"
            if params.get("Typ nadwozia"):
                car["chassis"] = params["Typ nadwozia"]
            else:
                car["chassis"] = "None"
            if params.get("Kolor"):
                car["color"] = params["Kolor"]
            else:
                car["color"] = "None"
            if params.get("Kraj pochodzenia"):
                car["import_country"] = params["Kraj pochodzenia"]
            else:
                car["import_country"] = "None"
            if params.get("Przebieg"):
                car["milage"] = int(''.join(filter(str.isdigit, params["Przebieg"])))
            else:
                car["milage"] = "None"
            yield car
        elif car["added"].date() < self.yesterday:
            self.old_cars_counter += 1

        if self.old_cars_counter >= self.break_after_old:
            raise scrapy.exceptions.CloseSpider(reason=f"Scraped {self.break_after_old} cars data from before yesterday")
