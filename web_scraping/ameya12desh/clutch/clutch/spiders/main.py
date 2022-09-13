#encoding=utf-8
from requests import Response
import scrapy 
import re
import logging

from datetime import datetime
from agenda_tools import get_schedule, download_images, get_category, months
from agenda_tools.get_schedule import remove_blank_spaces

pattern = re.compile(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,8}')


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year
dict_spa_eng_adv = months.dict_of_months_adv_spanish_to_english 



class Webscrape(scrapy.Spider):
    name = 'clutch'
    logger = logging.getLogger(name)

    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }


    start_urls = [  
                  'https://clutch.co/agencies/sem'
    ]



    def parse(self, response):
        links = set(response.xpath('//h3[@class="company_info"]/a/@href').getall())

        for idx,link in enumerate(links):
            self.logger.info(f'Link {idx+1}/{len(links)}')
            if link:
                # link = '{}{}'.format(base_url,link)
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links)})

        next_page = response.xpath('//li[@class="page-item next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            

    def parse_web(self, response, **kwargs):
        link = kwargs['link']
        title = kwargs['title']
        location = kwargs['location']
        location_google_maps = kwargs['location_google_maps']
        founded_year = kwargs['founded_year']
        number_emplyes = kwargs['number_emplyes']

        email_dirty = ' '.join(response.xpath('//*[contains(text(),"@")]/text()').getall())
        emails = re.findall(pattern,email_dirty)   
        email = ' / '.join(emails) 

        yield { 
                'Company name': title,
                'Location': location,
                'Location Google Maps': location_google_maps,
                'Year Founded': founded_year,
                'Website Link': link,
                'No. of employees':number_emplyes,
                'Emails': email
                
                }   


    def new_parse(self, response, **kwargs):
        link = kwargs['link']
        len_links = kwargs['len']
        idx = kwargs['idx']

        title = remove_blank_spaces(response.xpath('//h1/a/text()').get())
        try:
            location = remove_blank_spaces(response.xpath('//div[@class="field-location"]//span[@class="location-name"]/text()').get())
        except Exception:
            location = None
        location_google_maps =  response.xpath('//div[@class="field-location"]//div[@class="google-maps"]/img/@src').get()
        founded_year = remove_blank_spaces( response.xpath('//*[@data-content="<i>Founded</i>"]/span/text()').get())
        number_emplyes = remove_blank_spaces(response.xpath('//*[@data-content="<i>Employees</i>"]/span/text()').get())
        link_to_web = response.xpath('//h1/a/@href').get()
        
        yield response.follow(link_to_web, callback= self.parse_web, cb_kwargs={
            'link':link_to_web,
            'title':title,
            'location':location,
            'location_google_maps':location_google_maps,
            'founded_year':founded_year,
            'number_emplyes':number_emplyes
            })



        