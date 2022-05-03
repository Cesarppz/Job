import scrapy
from scrapy_playwright.page import PageCoroutine
import pickle
from agenda_tools.get_schedule import remove_blank_spaces


path = '/home/cesar/Documents/job/web_scraping/javier/hoteles/list_of_links.dat'

class MainPySpider(scrapy.Spider):
    name = 'camino_santiago'

    
    def start_requests(self):
        with open(path,'rb') as f:
            urls = pickle.load(f)
        for url in urls[:2]:
            for i in url['Link'][:2]:
                yield scrapy.Request(i, 
                meta = dict(playwright=True,
                        playwright_include_page = True,
                        playwright_page_coroutines = [
                            PageCoroutine('wait_for_timeout',5000),
                            PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
                        ]
                        ),cb_kwargs={'Name':url['Name']},callback=self.parse)
        

    def parse(self, response, **kwargs):
        name = kwargs['Name']
        title = response.xpath('//h2[@id="hp_hotel_name"]/text()').getall()
        title = remove_blank_spaces(' '.join(title))
        
        #Services
        #habitaciones = response.xpath('//div[@class="_e3ed6b426 _425b57dc7 d79b273389 _b7ed60b59"]/div[@class="_361c04b9c _729127938 _78cd05546"]//div[@class="_a11e76d75 c5cf92dd20"]/text()').getall()
        habitaciones = response.xpath('//div[@class="_e3ed6b426 _425b57dc7 d79b273389 _b7ed60b59"]').getall()
        capacidad = response.xpath('//div[@class="_361c04b9c _729127938 _10eb43c0c"]//div[@class="cea9cafb89"]/@aria-label').getall()
        
        
        # for idx_h, habitacion in enumerate(habitaciones):
        yield {
                'Title':title,
                'Habitaciones':habitaciones,
                'Capacidad':capacidad,
                'City':name
            }
 