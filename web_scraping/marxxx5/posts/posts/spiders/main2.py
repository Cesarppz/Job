from urllib import response
import scrapy
import logging

from scrapy_splash import SplashRequest

from datetime import datetime
import random
from agenda_tools.tools import remove_blank_spaces
from agenda_tools import  download_images
import pickle

logger = logging.getLogger(__name__)
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

class MainSpider(scrapy.Spider):
    name = 'posts2'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        with open('/home/cesarppz/Documents/jobs/web_scraping/mapandmarket/inmobiliaria/filename.pickle', 'rb') as handle:
            b = pickle.load(handle)
            for i in b:
                yield scrapy.Request(i, callback=self.parse )

    def parse(self, response):
        main_link = response.request.url
        print(main_link)

        if main_link == 'https://nursingpaperessays.com/blog/':
            print('Si')
            links = response.xpath('//h2[@class="title front-view-title"]/a/@href').getall()
            for idx, link in enumerate(links):
                if link:
                    logger.info(f'thirdlinks {main_link}/{idx}/{len(links)}')
                    yield response.follow(link, callback=self.third_parse, cb_kwargs={'product_link': link})
    
        else:
            box = []
            content = response.xpath('//div[@class="thecontent"]//text()').getall()

            for i in content:
                if i == 'Order Now':
                    break
                else:
                    box.append(i)

            content = remove_blank_spaces(' '.join(box))
            title = response.xpath('//h1/text()').get()

            yield {
                "post title":title,
                "post content": content
            }


    def third_parse(self, response):
        box = []
        content = response.xpath('//div[@class="thecontent"]//text()').getall()

        for i in content:
            if i == 'Order Now':
                break
            else:
                box.append(i)

        content = remove_blank_spaces(' '.join(box))
        title = response.xpath('//h1/text()').get()

        yield {
            "post title":title,
            "post content": content
        }