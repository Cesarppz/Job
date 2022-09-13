import scrapy
import logging

from scrapy_splash import SplashRequest

from datetime import datetime
import random
from agenda_tools.tools import remove_blank_spaces
from agenda_tools import  download_images
from scrapy_playwright.page import PageCoroutine


logger = logging.getLogger(__name__)
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

class MainSpider(scrapy.Spider):
    name = 'posts'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        url = 'https://nursingpaperessays.com/sitemap_index.xml'

        yield scrapy.Request(url=url, callback=self.parse, meta={
            'playwright':True, 
            'playwright_include_page':True, 
            'playwright_page_coroutines': [PageCoroutine('wait_for_selector','td')] 
            } 
            )

    async def parse(self, response):
        links = list(set(response.xpath('//td/a/@href').getall()))
        print(links)
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Link {idx}/{len(links)}')
                yield response.follow(link, callback=self.parse_main, cb_kwargs={'main_link':link, 'playwright_include_page':True})


    def parse_main(self,response, **kwargs):
        main_link = kwargs['main_link']
        main_link = main_link.split('/')[2]
        links = list(set( response.xpath('//td/a/@href').getall()))
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Sublinks {main_link}/{idx}/{len(links)}')
                yield response.follow(link, callback=self.second_parse, cb_kwargs={'product_link': link})
    

    def second_parse(self, response, **kwargs):
        main_link = kwargs['product_link']

        if main_link == 'https://nursingpaperessays.com/blog/':
            print('Si')
            links = response.xpath('//h2[@class="title front-view-title"]/a/@href').getall()
            for idx, link in enumerate(links):
                if link:
                    logger.info(f'thirdlinks {main_link}/{idx}/{len(links)}')
                    yield response.follow(link, callback=self.third_parse, cb_kwargs={'product_link': link})
    
        else:
            print('No')
            box = []
            content = response.xpath('//div[@class="thecontent"]/*[(not(@class) or @class!="order_discount_pane_wp" and @align!="center")]//text()').getall()
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
        content = response.xpath('//div[@class="thecontent"]/*[(not(@class) or @class!="order_discount_pane_wp" and @align!="center")]//text()').getall()
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