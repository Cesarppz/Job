from operator import ge
import scrapy 
import urllib
import subprocess
import re
import datetime as dt
import logging
import time
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from selenium import webdriver

logger = logging.getLogger()
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

pattern_geozone  = re.compile(r'Ciudad: (\w+) -')
main_url = 'https://zonadivas.mx'
# cop_pattern = re.compile(r'.*(COP|USD).*')


class Webscrape(scrapy.Spider):
    name = 'zonadivas'
    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        input_category = getattr(self,'category',None)
        # print('Input c',input_category)
        if input_category is None:
            input_category = 'todas'
        else:
            input_category = '-'.join(input_category.split()).lower()
        
        # if input_category == 'escorts-y-putas':
        #     input_category = 'escorts'

        input_geozone = getattr(self,'geo_zone',None)
        if input_geozone is None:
            input_geozone = 'todas'
        else:
            input_geozone = '-'.join(input_geozone.split()).lower()

        if input_category == 'todas' and input_geozone == 'todas':
            url = main_url
        elif input_category == 'todas' and input_geozone != 'todas':
            url = f'{main_url}/escorts-en-{input_geozone}/'
        elif input_geozone == 'todas' and input_category != 'todas':
            url = f'{main_url}/escorts-en-{input_category}/'
        # else:
        #     url = f'{main_url}/{input_category}/{input_geozone}/'
        
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        links = set(response.xpath('//a[@class="tg-element-absolute"]/@href').getall())
        for idx, link in enumerate(links):
            logger.info(f'Links {idx} / {len(links)}')
            yield response.follow(link, callback=self.new_parse,cb_kwargs={'link':link})
            
 
        
        # next_page = response.xpath('//a[@id="button_arrow_pagination"]/@href').get()
        # if next_page:
        #     yield response.follow(next_page, callback= self.parse)


    def new_parse(self, response, **kwargs):
        link = kwargs['link']

        
        title = response.xpath('//h1/span/text()').get()
        try:
            geo_zone = ' - '.join(response.xpath('//div[@class="grve-element grve-text"]//text()').getall()).strip().replace('\n','')
            geo_zone = re.findall(pattern_geozone,geo_zone )[0]
        except:
            geo_zone = None
        #Categoria
        category =  geo_zone
        #Description
        try:
            description = self.remove_spaces(' '.join(response.xpath('//div[@class="grve-element grve-text"]//text()').getall()))
        except:
            description = None
        phone =  response.xpath('//div[@class="grve-element grve-text"]//strong/text()').get().replace('Tel: ','')
        try:
            whatsapp = response.xpath('//span[text()="CONT??CTAME POR WHATSAPP AHORA"]/parent::a/@href').get()
        except:
            whatsapp = None
        email = None
        

        yield{
            'Categoria del Anuncio':category,
            'Zona Geografica (Estado y Ciudad)':geo_zone,
            'Titulo del Anuncio':title,
            'Descripcion del Anuncio':description,
            'Telefono de Contacto':phone,
            'WhatsApp de Contacto Numero':phone,
            'Link WhatsApp de Contacto Anuncio':whatsapp,
            'Email de Contacto':email,
            'ID Anuncio':None,
            'Url del Anuncio':link,
            'Nombre de la P??gina':'Zonadivas'
            }

        
    def remove_spaces(self,x):
        return x.replace('  ',' ').replace('\r','').replace('\t','').replace('\xa0','').replace('\n','').strip()


