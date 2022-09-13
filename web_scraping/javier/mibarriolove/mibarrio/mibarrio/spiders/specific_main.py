import scrapy
import logging

from datetime import datetime
import random
from agenda_tools.tools import remove_blank_spaces
from agenda_tools import  download_images


logger = logging.getLogger(__name__)
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

class MainSpider(scrapy.Spider):
    name = 'mibarrio_products'
    custom_settings= {
                        # 'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        # 'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    start_urls = ['https://www.mibarrio.love/tienda/maria-rodriguez/']

    # def parse(self, response):
    #     links = list(set(response.xpath('//ul[@id="menu-comercio-local"]/li/a/@href').getall()))
    #     for idx, link in enumerate(links):
    #         if link:
    #             logger.info(f'Link {idx}/{len(links)}')
    #             yield response.follow(link, callback=self.parse_main, cb_kwargs={'main_link':link})


    # def parse_main(self,response, **kwargs):
    #     main_link = kwargs['main_link']
    #     links = set(response.xpath('//div[@class="seller-listing-content sdfsdf"]/ul/li[@id="dokan_vendor_position"]//h2/a/@href').getall())
    #     for idx, link in enumerate(links):
    #         if link:
    #             logger.info(f'Sublinks {main_link}/{idx}/{len(links)}')
    #             yield response.follow(link, callback=self.second_parse, cb_kwargs={'product_link': link})
    

    def parse(self, response):
        # main_link = kwargs['product_link']

        logo = response.xpath('//div[@class="divine-store-image profile-img "]/img/@src').get()
        negocio_name = response.xpath('//h1[@class="store-name"]/text()').get()
        negocio_name = '_'.join(negocio_name.split(' ')).lower()
        title_for_logo  = ''.join(response.xpath('//h1/text()').get().lower().split(' '))
        logo_name = download_images.download(logo, title_for_image=title_for_logo, nombre_del_lugar=negocio_name)

        links = response.xpath('//div[@class="seller-items"]/ul/li//div[@class="mf-product-thumbnail"]/a/@href').getall()
        for idx, link in enumerate(links):
            if link:
                logger.info(f'Products {idx}/{len(links)}')
                yield response.follow(link, callback=self.last_parse, cb_kwargs={'logo':logo_name, 'negocio_name':negocio_name})


    def last_parse(self, response, **kwargs):
        logo_name = kwargs['logo']
        negocio_name = kwargs['negocio_name']

        title    = remove_blank_spaces(response.xpath('//h1/text()').get())
        try:
            sku      = remove_blank_spaces(response.xpath('//li[contains(.,"SKU")]/span/text()').get())
        except Exception:
            sku  = None
        vendedor = remove_blank_spaces( response.xpath('//div[@class="sold-by-meta"]/a/text()').get())
        try:
            price =  remove_blank_spaces(response.xpath('//div[@class="summary entry-summary"]/*[@class="price"]//span[@class="woocommerce-Price-amount amount"]/text()').get()) + ' €'
        except Exception:
            price = None
        short_description = remove_blank_spaces( ' '.join(response.xpath('//div[@class="woocommerce-product-details__short-description"]/p//text()').getall()))
        try:
            large_description = remove_blank_spaces(' '.join(response.xpath('//div[@id="tab-description"]/p//text()').getall()))
        except Exception:
            large_description = None
        image =  response.xpath('//div[@class="woocommerce-product-gallery__image"]//img/@src').get()
        

        title_for_image = ''.join(title.lower().split(' ')) + str(random.randint(0,1000))
        title_for_image =  title_for_image.replace('/','')
        image_name = download_images.download(image, title_for_image=title_for_image, nombre_del_lugar=negocio_name)


        yield{
            'Title': title,
            'SKU':sku,
            'Vendedor':vendedor,
            'Price':price,
            'Short Description':short_description,
            'Long Description':large_description,
            'Image Name':image_name,
            'Logo Name':logo_name,
            'Negocio Name':negocio_name
        }


        