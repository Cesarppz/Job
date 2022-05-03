from operator import ge
import scrapy 
import urllib
import subprocess
import re
import datetime as dt
import logging

from playwright.sync_api import sync_playwright
from scrapy.crawler import CrawlerProcess
from datetime import datetime

logger = logging.getLogger()
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

main_url = 'https://www.outletdeviviendas.com'
pattern = re.compile(r'.*\((.*)\)')
patter_url = re.compile(r'.*\/tipo-(\w+)/.*')
pattern2  = re.compile(r'.*\s(\w+)')

class Webscrape(scrapy.Spider):
    name = 'inmobiliaria_outlet'
    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    start_urls = [ 
            main_url
     ]
   # allowed_domains = ['https://mx.mundosexanuncio.com/']

    def parse(self, response):
        links = response.xpath('//div[@id="prefoot"]//li/a/@href').getall()
        for idx, link in enumerate(links):
            logger.info(f'links {idx} / {len(links)}')
            #link = '{}{}'.format(main_url,link)
            yield response.follow(link, callback=self.f_parse,cb_kwargs={'type':None})
       

    def f_parse(self, response, **kwargs):
        if kwargs['type'] == None:
            type_c = response.request.url
            type_c = re.match(patter_url,type_c).group(1)
        else:
            type_c = kwargs['type']
        

        city = response.xpath('//h1[@class="fs_22 colact mar0 pad0"]/text()').get()
        try:
            city = re.match(pattern, city).group(1)
        except AttributeError:
            city = re.match(pattern2, city).group(1)

        links = response.xpath('//a[@class="blq t94 padlr3p"]/@href').getall()
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Link {idx+1}/{len(links)}')
               # link = '{}{}'.format(main_url,link)
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link,'city':city,'type':type_c})

        
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            next_page = '{}{}'.format(main_url,next_page)
            yield response.follow(next_page, callback= self.f_parse,cb_kwargs={'type':type_c})


    def new_parse(self, response, **kwargs):
        city = kwargs['city']
        type_c = kwargs['type']
        #Precio
        price = response.xpath('//div[@class="blq mart4 fs_25 colpri txt_a_r"]/span/text()').get().strip()
        #locate
        location = response.xpath('//div[@class="blq t99 padl1p mart4 fs_13 colpri"]/text()').get().strip()
        #Nombre
        name = response.xpath('//h1[@class="blq fs_23"]/text()').get()
        #space
        space_t = response.xpath('//div[@class="blq mart32 colpri marb6"][text()="CARACTERÍSTICAS"]/following-sibling::div[@class="bl_izq t50 colpri"]/div/text()').getall()
        slice_d = int(len(space_t) / 2)
        space_t = space_t[:slice_d]
        if len(space_t) > 1:
            if space_t[1] != space_t[-1]:
                space = ' '.join([space_t[1].strip(),space_t[2].strip()])
            else:
                space = space_t[1]
        else:
            space = None
        #Image
        image = response.xpath('//div[@id="carousel-rotacion"]//img/@src').get()
        #Metros
        size = space_t[0].strip()

        yield{
            'Nombre':name,
            'Location':location,
            'Price':price,
            'Metros cuadrados':size,
            'Espacios':space,
            'City':city,
            'Images':image,
            'Tipo':type_c
        }

