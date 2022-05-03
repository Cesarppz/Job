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

main_url = 'https://www.inmobiliariabancaria.com'
pattern = re.compile(r'https://www.inmobiliariabancaria.com/(.*)')


class Webscrape(scrapy.Spider):
    name = 'inmobiliaria'
    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    start_urls = [ 
        'https://www.inmobiliariabancaria.com/pisos-bancos',
        'https://www.inmobiliariabancaria.com/pisos-venta',
        'https://www.inmobiliariabancaria.com/casas-bancos',
        'https://www.inmobiliariabancaria.com/aticos-bancos',
        'https://www.inmobiliariabancaria.com/duplex-bancos',
        'https://www.inmobiliariabancaria.com/chalet-bancos',
        'https://www.inmobiliariabancaria.com/garaje-bancos',
        'https://www.inmobiliariabancaria.com/locales-venta',
        'https://www.inmobiliariabancaria.com/naves-industriales',
        'https://www.inmobiliariabancaria.com/terrenos-venta'
     ]
   # allowed_domains = ['https://mx.mundosexanuncio.com/']

    def parse(self, response):
        type_c = response.request.url
        type_c = re.match(pattern, type_c).group(1)
        province = response.xpath('//ul[@class="list-unstyled"]//strong/text()').getall()
        for idx_p, i in enumerate(province):
            idx_p += 1
            links = response.xpath(f'//div[@class="col-md-8"]//ul[@class="list-unstyled"][{idx_p}]/li/a/@href').getall()
            for idx, link in enumerate(links):
                logger.info(f'links {idx} / {len(links)}')
                link = '{}{}'.format(main_url,link)
                yield response.follow(link, callback=self.s_parse, cb_kwargs={'province':i,'type_c':type_c})
       


    def s_parse(self, response, **kwargs):
        province = kwargs['province']
        type_c = kwargs['type_c']
        links = set(response.xpath('//h3/preceding-sibling::ul[@class="list-unstyled"]//a/@href').getall())
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Link {idx+1}/{len(links)}')
                link = '{}{}'.format(main_url,link)
                yield response.follow(link, callback=self.f_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links),'province':province,'type_c':type_c})


    def f_parse(self, response, **kwargs):
        province = kwargs['province']
        type_c = kwargs['type_c']
        link = kwargs['link']
        len_links = kwargs['len']
        idx_link = kwargs['idx']
        city = response.xpath('//a[@id="dropLocalidad"]//text()').get().strip()
        links = response.xpath('//div[@class="col-md-8"]//div[@class="card m-b-lg p-r-md"]//h3/a/@href').getall()
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Link {idx+1}/{len(links)}')
                link = '{}{}'.format(main_url,link)
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links),'province':province,'city':city,'type_c':type_c})

        
        next_page = response.xpath('//a[@title="Siguiente"]/@href').get()
        if next_page:
            next_page = '{}{}'.format(main_url,next_page)
            yield response.follow(next_page, callback= self.f_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links),'province':province,'type_c':type_c})


    def new_parse(self, response, **kwargs):
        province = kwargs['province']
        type_c = kwargs['type_c']
        link = kwargs['link']
        city = kwargs['city']

        #Precio
        price = response.xpath('//div[@style="font-size:2.8em;margin-top:0;color:#FF0288;font-weight:bold;"]/text()').get().strip()
        #locate
        location = response.xpath('//h3[@class="text-overflow"]/text()').get().strip()
        #Nombre
        name = response.xpath('//h2[@style="font-size:1.5em;font-weight:bold;"]/text()').get().strip()
        #space
        espacio_disponible = response.xpath('//table[@class="table table-striped"]//tr[contains(.,"Dispone")]/th//text()').getall()
        espacio_disponible = ' '.join(espacio_disponible)
        #Eficiencia energetica
        eficiencia_e = response.xpath('//table[@class="table table-striped"]//tr[contains(.,"Eficiencia energética")]/th//text()').get()
        #Image
        image = response.xpath('//div[@class="col-sm-6"]//img/@src').getall()
        #Metros
        size = response.xpath('//span[@class="label label-success"]/text()').get()
        #precios por metros
        precio_por_metro = ' - '.join(response.xpath('//table[@class="table table-striped"]//tr[contains(.,"Superficie")]//text()').getall()[1:])
        # Habitaciones
        n_habitaciones = response.xpath('//span[@class="label label-warning"][@title="Habitaciones"]/text()').get()
        # Baños
        n_bathrooms = ' '.join(response.xpath('//span[@title="Baños"]//text()').getall())
        #Descripcion
        description = response.xpath('//div[@class="col-sm-6"]/h2/following-sibling::p/text()').get().strip()

        yield{
            'Nombre':name,
            'Location':location,
            'Price':price,
            'Metros cuadrados':size,
            'Numero de Baños':n_bathrooms,
            'Numero de habitaciones':n_habitaciones,
            'Espacio Disponible':espacio_disponible,
            'Eficiencia Electrica':eficiencia_e,
            'precio por metro':precio_por_metro,
            'Province':province,
            'City':city,
            'Images':image,
            'Descripcion':description,
            'Tipo':type_c
        }

