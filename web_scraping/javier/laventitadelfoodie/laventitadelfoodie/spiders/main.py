import scrapy
import logging
import re 
import random
from agenda_tools.get_schedule import remove_blank_spaces
from datetime import datetime
from agenda_tools.download_images import download
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
pattern = re.compile(r'.*\/\d+-(.*)')

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year


class MainSpider(scrapy.Spider):
    name = 'laventitadelfoodie'
    #allowed_domains = ['https://www.laventitadelfoodie.com']
    start_urls = ['http://www.laventitadelfoodie.com/']

    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }

    def parse(self, response):
        links = response.xpath('//ul[@id="top-menu"]/li[@class="category"]/a/@href').getall()
        for idx, link in enumerate(links):
            category_name = re.match(pattern,link).group(1)
            logger.info(f'Category {idx+1}/{len(links)}: {category_name}')
            yield response.follow(link, callback=self.parse_main, cb_kwargs={'category_name':category_name})


    def parse_main(self, response, **kwargs):
        category_name = kwargs['category_name']
        links_main = set(response.xpath('//div[@class="products row"]/article[@class="product-miniature js-product-miniature"]//h2/a/@href').getall())
        for idx_m, link in enumerate(links_main):
            logger.info(f'Producto {idx_m+1}/{len(links_main)}')
            yield response.follow(link, callback=self.new_parse, cb_kwargs={'category_name':category_name,'link':link})

        next_page = response.xpath('//ul[@class="page-list clearfix text-sm-center"]/li[last()]/a[@class="next js-search-link"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_main, cb_kwargs={'category_name':category_name}    )


    def new_parse(self, response, **kwargs):
        category = kwargs['category_name']
        link = kwargs['link']
        # idx = kwargs['idx']
        # len_links = kwargs['len']

        title = response.xpath('//h1/text()').get()
        price = response.xpath('//div[@class="current-price"]/span/text()').get().replace('\xa0',' ')
        description = remove_blank_spaces(' '.join(list(set(response.xpath('//div[@itemprop="description"]//text()').getall())))).replace('  ',' ')
        image = response.xpath('//div[@class="product-cover"]/img/@src').get()
        title_for_image = '_'.join(title.split())+str(random.randint(1,100))
        images_name = download(image=image,title_for_image=title_for_image, nombre_del_lugar='laventitadelfoodie')
        short_description = remove_blank_spaces(' '.join(list(set(response.xpath('//div[@itemprop="description"]/div[@class="value"][1]//text()').getall())))).replace('  ',' ')
        
        yield {
            'Nombre Producto': title, 
            'Categoria':category,
            'Precio':price,
            'SKU':None,
            'Descripcion':description,
            'Short Description':short_description,
            'Imagen':images_name,
            'Link':link
        }
