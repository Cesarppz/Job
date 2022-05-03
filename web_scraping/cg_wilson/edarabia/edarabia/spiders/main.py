import scrapy 
import urllib
import subprocess
import re
import logging
import time
import datetime as dt

from datetime import datetime
from scrapy_splash import SplashRequest
from agenda_tools import get_schedule, download_images, get_category, tools
from agenda_tools.get_schedule import remove_blank_spaces
from selenium import webdriver
from requests_html import HTMLSession
session = HTMLSession()


mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

mes_pattern = re.compile(r'de ([a-z]+)')
pattern_year = re.compile(r'\d{4,4}')
pattern_schedule = re.compile(r'(\d+\sd?e?\s?(\w+)?( de \d+)?( al)?( \d+ de \w+ de \d+)?)')
pattern = re.compile(r'(^http.*\.\w{3})(.*)')
patter_style = re.compile(r'background-image:url\((.*\.\w{3}).*')
pattern_url1 = re.compile(r'https://caixaforum.org/es/madrid/familia.*')
pattern_url2 = re.compile(r'https://caixaforum.org/es/madrid/exposiciones.*')

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
     #              datefmt='%Y-%m-%d %H:%M')


class Webscrape(scrapy.Spider):
    name = 'edarabia'
   

    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }

    start_urls = ['https://www.edarabia.com/schools/']

    # def start_requests(self):
    #     url_r = 'https://www.edarabia.com/schools'

    #     yield SplashRequest(url=url_r, callback=self.parse )
    

    def parse(self, response, **kwargs):
        links = response.xpath('//div[@class="list-items"]/div[@class="row"]//h3/a/@href').getall() 
        #images = response.xpath('//div[@class="w-post-elm post_image usg_post_image_1 stretched"]//img/@src').getall()
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Link {idx}/{len(links)}')
                #image = re.match(pattern, image).group(1)
                #link = 'https://www.mncn.csic.es/{}'.format(link)
                
                yield response.follow(link, callback=self.middle_page_parse) #,cb_kwargs={'link':link, 'idx':idx+1,'len':len(links)})#, 'image':images[idx]})
        
    def middle_page_parse(self, response, **kwargs):
        try:
            last_number_pages = kwargs['number_pages']
        except KeyError:
            last_number_pages = 0

        if last_number_pages is None:
            last_number_pages = 0

        page = response.xpath('//div[@class="list-items"]/div[@class="row"]/div[@class="col-md-10 col-sm-10 col-xs-10"]/div[@class="row"]//h5/a/@href').getall()
        for idx_p, pg in enumerate(page):
            if pg:
                logger.info(f'Page {idx_p + 1}/{len(page)}')
                yield response.follow(pg, callback=self.new_parse, cb_kwargs={'number_pages_id':idx_p+number_pages,'number_pages_len':len(page)+number_pages})
                # yield SplashRequest(pg, callback=self.new_parse, cb_kwargs={'number_pages_id':idx_p+number_pages,'number_pages_len':len(page)+number_pages})

        number_pages = len(page) + last_number_pages

        next_page = response.xpath('//a[@title="Next"]/@data-page').get()
        if next_page:
            next_page = 'https://www.edarabia.com/schools/uae/?pg={}'.format(next_page)   
            yield response.follow(next_page, callback=self.middle_page_parse,cb_kwargs={'number_pages':number_pages})    
            #yield SplashRequest(pg, callback=self.middle_page_parse)

    def new_parse(self, response, **kwargs):
        # link = kwargs['link']
        # len_links = kwargs['len']
        # idx = kwargs['idx']
        idx = kwargs['number_pages_id']
        len_page = kwargs['number_pages_len']

        logger.info(f'Scraping {idx}/{len_page}')

        leadership = response.xpath('//li[contains(.,"Leadership: ")]//text()').getall()
        if leadership:
            leadership = leadership[1]
        else:
            leadership = None
        school_name = response.xpath('//div[@class="content-box-m0"]//h1/text()').get() 
        address = response.xpath('//div[@class="content-box-m0"]//li[contains(.,"Address: ")]//text()').getall()[1:5]
        address = ' '.join(address)
        tel =  response.xpath('//div[@class="content-box-m0"]//li[contains(.,"Tel: ")]//text()').getall()
        tel = remove_blank_spaces(' '.join(tel).split('\n')[0].replace('Show Number','') )
        website = response.xpath('//a[@title="Visit Website"]/@href').get()

        yield {
            'school_name':school_name,
            'Leadership':leadership,
            'Address':address,
            'Tel':tel,
            'Website': website
        }


