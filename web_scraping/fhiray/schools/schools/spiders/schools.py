from attr import Attribute
import scrapy 
from scrapy.crawler import CrawlerProcess
import urllib
import subprocess
import re
import logging
import datetime as dt
from datetime import datetime
from agenda_tools import get_title, get_schedule, download_images, get_category
logger = logging.getLogger()

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

link_image_pattern = re.compile(r'^(https?).*/(.+\.(jpg|jpeg|png))')
patter_links = re.compile(r'^(http).*//.*\/((exposiciones|cine-en-casa-de-mexico|literatura|familias|teatro))/.*')
pattern_schedule = re.compile(r'\d+\s+de\s+\w+')
#pattern_horario = re.compile(r'(([A-Za-záéíóú]+ )?\d+( de [A-Za-záéíóú]+)?)( y \d+ de [A-Za-záéíóú]+)?( a las \d+:\d+)?')
pattern_horario = re.compile(r'([A-Za-záéíóú]+ \d+ de [A-Za-záéíóú]+)( y \d+ de [A-Za-záéíóú]+)?( a las \d+:\d+)?')


class Webscrape(scrapy.Spider):
    name = 'schools'
    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }
    start_urls = [  
                  'https://web.khda.gov.ae/en/Education-Directory/Schools',
                  'https://web.khda.gov.ae/en/Education-Directory/Higher-Education'
                  ]


    def parse(self, response):
        if response.request.url == 'https://web.khda.gov.ae/en/Education-Directory/Schools':
            type = 'Schools'
        else:
            type = 'University'

        links = set(response.xpath('//a[@id="lnkName"]/@href').getall())
        for idx, link in enumerate(links):
            logger.info(f'Link {idx+1}/{len(links)}')
            if link:
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links),'type':type})


    def new_parse(self, response, **kwargs):
        type = kwargs['type']
        link = kwargs['link']
        len_links = kwargs['len']
        idx = kwargs['idx']

        if type == 'Schools':
            school_name =  response.xpath('//h2[@class="filter-details__title"]/text()').get()
            location = ' '.join(response.xpath('//li[contains(.,"                            Location")]/span/address//text()').getall()).strip()
            email =  response.xpath('//li[contains(.,"                            Email")]/span/a/text()').get().strip()
            try:
                phone =  response.xpath('//li[contains(.,"                            Call")]/span/a/text()').get().strip()
            except AttributeError:
                phone = None
            curriculum =  response.xpath('//li[contains(.,"Curriculum ")]/span/text()').get()
            grade =  response.xpath('//li[contains(.,"Grade ")]/span/text()').get()

            yield {
                    'Type': type,
                    'school name':school_name,
                    'Location':location,
                    'Email':email,
                    'Telephone': phone,
                    'Curriculum': curriculum,
                    'Grade\Year':grade
                    
                    }
        else:
            university_type =  response.xpath('//li[contains(.,"Type")]/span/text()').get()
            name =  response.xpath('//h2[@class="filter-details__title"]/text()').get()
            location = ' '.join(response.xpath('//li[contains(.,"                            Location")]/span/address//text()').getall()).strip()
            established = response.xpath('//li[contains(.,"Established")]/span/text()').get()
            try:
                phone =  response.xpath('//li[contains(.,"                            Call")]/span/a/text()').get().strip()
            except AttributeError:
                phone = None
            email =  response.xpath('//li[contains(.,"                            Email")]/span/a/text()').get().strip()

            yield {
                'Type':type,
                'Name':name,
                'University Type':university_type,
                'Location':location,
                'Established':established,
                'Telephone': phone,
                'Email':email

            }


