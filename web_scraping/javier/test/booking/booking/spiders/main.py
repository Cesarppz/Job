import scrapy 
import urllib
import subprocess
import re
import logging
import time
import datetime as dt
import random

from datetime import datetime
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
pattern = re.compile(r'sede.*')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

class Webscrape(scrapy.Spider):
    name = 'booking'
    logger = logging.getLogger(__name__)

    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }
    
    start_urls = ['https://www.booking.com/searchresults.es.html?aid=304142;label=gen173nr-1BCAEoggI46AdIM1gEaEaIAQGYAQq4AQfIAQ3YAQHoAQGIAgGoAgO4ArGuuo8GwAIB0gIkNTdjNTQyMTEtMTZlYy00YWFkLTg4ZjAtZTY1MDQ2YzhlODQw2AIF4AIB;sid=d66a016dcaeb9f47c6acc13833910118;checkin=2022-02-01;checkout=2022-02-28;dest_id=769;dest_type=region;srpvid=8957561da3bb048d;ss=navarre&']


    def parse(self, response, **kwargs):

        links = response.xpath('//a[@class="fb01724e5b"]/@href').getall()    
        print('Links:', links)   
        #images = response.xpath('//div[@class="w-post-elm post_image usg_post_image_1 stretched"]//img/@src').getall()
        for idx, link in enumerate(links):
            #xpath = 
            self.logger.info(f'Link {idx+1}/{len(links)}')
            if link:
                self.logger.info(f'Link {idx}/{len(links)}')
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links)})#, 'image':images[idx]})
    

    def get_links_by_scralling(self,url,xpath_expresion, attribute='href'):
        #Instanciar el navegador
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        driver = webdriver.Firefox(executable_path='../driver/geckodriver', options=options)
        driver.get(url)

        #Get links scralling
        box = []
        previous_heigth = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(5)
            new_heigth = driver.execute_script('return document.body.scrollHeight')
            if new_heigth == previous_heigth:
                box.extend(driver.find_elements_by_xpath(xpath_expresion))
                break
            previous_heigth = new_heigth
        box = [i.get_attribute(attribute) for i in box[1:]]
        driver.close()
        return box

    def get_attribute_by_selenium(self,url,xpath_expresion,text=True,list_number=0):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='/home/cesar/Documents/job/web_scraping/javier/agenda/driver/geckodriver', options=options)
        driver.get(url)
        time.sleep(1.5)

        if list_number == 1:
            result = driver.find_elements_by_xpath(xpath_expresion)
            result = ' / '.join([i.text for i in result if i != ''])
            print('Result :',result)
            driver.close()
            return result
        elif list_number == 0:
            result = driver.find_elements_by_xpath(xpath_expresion)[0].text
            driver.close()
            print('Result :',result)
            return result

    def new_parse(self, response, **kwargs):
        link = kwargs['link']
        len_links = kwargs['len']
        idx = kwargs['idx']

        print('Url :',link)
        name = remove_blank_spaces(' '.join(response.xpath('//h2[@id="hp_hotel_name"]/text()').getall()))
        address = remove_blank_spaces(response.xpath('//p[@class="address address_clean"]/span/text()').get()) 
        type_of_service = self.get_attribute_by_selenium(link,'//a[@class="_4310f7077 _45807dae0 d1e16e79fc js-legacy-room-name _f7538b398"]/span',list_number=1)
        if type_of_service is None:
            type_of_service = self.get_attribute_by_selenium(link,'//table//span[@class="hprt-roomtype-icon-link "]',list_number=1)
            if type_of_service is None:
                type_of_service = self.get_attribute_by_selenium(link,'//div[@class="room-info"]',list_number=1)
        yield {
            'Name':name,
            'address':address,
            'Type of Room':remove_blank_spaces(type_of_service)
        }