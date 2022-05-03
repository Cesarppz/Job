import scrapy
import logging
import re

from agenda_tools.get_schedule import remove_blank_spaces
from datetime import datetime
from scrapy_proxy_pool.policy import BanDetectionPolicy

logger = logging.getLogger(__name__)

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year  

pattern = re.compile(r'^.css.*')

class ForkRestaurant(scrapy.Spider):
    name = 'fork'
    start_urls = ['https://www.thefork.es/search/?cityId=328022']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }

    def start_requests(self):
        for i in range(1,51):
            url = 'https://www.thefork.es/search/?cityId=328022&p={}'.format(i)
            logger.info(f'Starting requests {i}')
            yield scrapy.Request(url,self.parse)

    def parse(self, response):
        links = response.xpath('//h2/a/@href').getall()
        print(links)
        for idx, link in enumerate(links):
            logger.info(f'Link {idx+1}/{len(links)}')
            if link:
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links)})

    def new_parse(self,response, **kwargs):
        link = kwargs['link']
        name = response.xpath('//h1/text()').get()
        category = response.xpath('//p[@class="css-zmb4ti eulusyj0"]/span[@class="css-17qrp4o e1xxesyf0"]/span[@data-test="restaurant-page-restaurant-tags-CUISINE"]/a/span/text()').get()
        mean_price = remove_blank_spaces(response.xpath('//span[contains(.,"Precio medio")]/following-sibling::span/text()').get())
        oferta = remove_blank_spaces(response.xpath('//div[@class="css-3o5z22 e1xxesyf0"]/p/text()').get()).capitalize()
        address = remove_blank_spaces(' '.join(response.xpath('//span[@class="eeio5r41 css-1juo9mb e1xxesyf0"]/span[@class="css-1lnlsqc eulusyj0"]/text()').getall()))
        link = '{}/menu'.format(link)
        image = response.xpath('//div[@class="slick-slide slick-active slick-current css-p4f2pd e1yrdu3r0"]/img/@src').get()
        dict_data = {
            'name':name,
            'category':category,
            'mean_price':mean_price,
            'oferta':oferta,
            'address':address,
            'image':image
        }
        yield response.follow(link, callback=self.get_menu, cb_kwargs=dict_data)

    def get_menu(self,response,**kwargs):
        menu = response.xpath('//dl[@class="css-1ndrudv e1xxesyf0"]/div[@class="css-1iqq28q elkhwc30"]//text()').getall()
        menu = [remove_blank_spaces(i) for i in menu if not re.match(pattern,i)]
        menu_plates = menu[::2]
        menu_prices = menu[1::2]
        menu = list(zip(menu_plates,menu_prices))
        menu = '  /  '.join(menu)
        kwargs['menu'] = menu
        yield kwargs

        
