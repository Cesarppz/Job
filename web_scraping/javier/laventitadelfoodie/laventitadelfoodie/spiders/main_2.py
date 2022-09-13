import scrapy
import logging
import re 
import random
from agenda_tools.tools import remove_blank_spaces
from datetime import datetime
from agenda_tools.download_images import download
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
pattern = re.compile(r'.*\/\d+-(.*)')

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year


class MainSpider(scrapy.Spider):
    name = 'comanderbbq'
    #allowed_domains = ['https://www.laventitadelfoodie.com']
    start_urls = ['https://comanderbbq.com']

    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }

    def parse(self, response):
        links = set( response.xpath('//li[@id="menu-item-423"]//ul[@class="sub-menu nav-dropdown nav-dropdown-default"]//a/@href').getall())
        for idx, link in enumerate(links):
            logger.info(f'Category {idx+1}/{len(links)}')
            yield response.follow(link, callback=self.parse_main)


    def parse_main(self, response, **kwargs):
        if response.request.url == 'https://comanderbbq.com/bbq-pit-boxdistribuidores-exclusivos-de-bbq-pit-box-en-espana/':
            middle_links = response.xpath('//a[@class="button primary"]/@href').getall()
            for m_link in middle_links:
                yield response.follow(m_link, callback=self.parse_main)

        links_main = response.xpath('//p[@class="name product-title woocommerce-loop-product__title"]/a/@href').getall()
        for idx_m, link in enumerate(links_main):
            logger.info(f'Producto {idx_m+1}/{len(links_main)}')
            yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link})

        next_page = response.xpath('//a[@class="next page-number"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_main)


    def new_parse(self, response, **kwargs):
        link = kwargs['link']
        # idx = kwargs['idx']
        # len_links = kwargs['len']

        title = remove_blank_spaces(response.xpath('//h1[@class="product-title product_title entry-title"]/text()').get())
        print(title)
        price = ' '.join(response.xpath('//p[@class="price product-page-price "]//text()').getall()).replace('\xa0',' ').replace('\n','').replace('  ',' ').strip()
        category = ' - '.join(response.xpath('//span[@class="posted_in"]/a/text()').getall())
        description = remove_blank_spaces(' '.join(response.xpath('//div[@id="tab-description"]//text()').getall())).replace('Descripción:  ','').replace('                                     ',' ').replace('  ',' ').strip().replace('Descripción','').replace('DESCRIPCIÓN','').replace('  ',' ').replace('       ',' ').replace('       ',' ').strip()
        image = response.xpath('//figure//img/@src').getall()[0]
        sku = response.xpath('//span[@class="sku_wrapper"]//span/text()').get()
        title_for_image = ('_'.join(title.split())+str(random.randint(1,100))).replace('/','_').replace('__','_')
        print('Title',title_for_image)
        images_name = download(image=image,title_for_image=title_for_image, nombre_del_lugar='comanderbbq')
        short_description = remove_blank_spaces(' '.join(response.xpath('//div[@class="product-short-description"]//text()').getall()))
        
        yield {
            'Nombre Producto': title, 
            'Categoria':category,
            'Precio':price,
            'SKU':sku,
            'Descripcion':description,
            'Short Description':short_description,
            'Imagen':images_name,
            'Link':link
        }
