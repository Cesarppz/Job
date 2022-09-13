import scrapy
import logging
import re
import time

from scrapy_splash import SplashRequest
from agenda_tools.get_schedule import remove_blank_spaces
from agenda_tools import  download_images
from datetime import datetime
from selenium import webdriver


options = webdriver.FirefoxOptions()
options.add_argument('--private')
#options.add_argument('--no-sandbox')
# options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0')
# options.add_argument("--headless")
driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

logger = logging.getLogger()

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

class MainPySpider(scrapy.Spider):
    name = 'dafiti'
    #start_urls = ['https://www.google.com/search?q=site%3Adafiti.com.co+%22montgreen%22&sxsrf=ALiCzsa6Aupu3tY9J7sCZX4BoqsOCj_Q4A%3A1658440478274&source=hp&ei=HsvZYpP2Dd6XhbIPuq6T4Aw&iflsig=AJiK0e8AAAAAYtnZLoHkh1q4ha4WnH_92To6tqJR0o4u&ved=0ahUKEwiT_dec_Ir5AhXeS0EAHTrXBMwQ4dUDCAo&uact=5&oq=site%3Adafiti.com.co+%22montgreen%22&gs_lcp=Cgdnd3Mtd2l6EANQAFgAYJIEaABwAHgAgAEoiAEokgEBMZgBAKABAqABAQ&sclient=gws-wiz']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}


    def start_requests(self):
        urls = [
            'https://www.google.com/search?q=site%3Adafiti.com.co+%22montgreen%22&sxsrf=ALiCzsa6Aupu3tY9J7sCZX4BoqsOCj_Q4A%3A1658440478274&source=hp&ei=HsvZYpP2Dd6XhbIPuq6T4Aw&iflsig=AJiK0e8AAAAAYtnZLoHkh1q4ha4WnH_92To6tqJR0o4u&ved=0ahUKEwiT_dec_Ir5AhXeS0EAHTrXBMwQ4dUDCAo&uact=5&oq=site%3Adafiti.com.co+%22montgreen%22&gs_lcp=Cgdnd3Mtd2l6EANQAFgAYJIEaABwAHgAgAEoiAEokgEBMZgBAKABAqABAQ&sclient=gws-wiz',
            'https://www.google.com/search?q=site:dafiti.com.co+%22montgreen%22&sxsrf=ALiCzsbJG3RYemtiszfgJJXi-UZV5ayM7g:1658619526124&ei=hobcYuygB8-kwbkP76KTiA4&start=10&sa=N&ved=2ahUKEwjs-6-dl5D5AhVPUjABHW_RBOEQ8NMDegQIARBF&biw=1536&bih=739&dpr=1.25',
            'https://www.google.com/search?q=site:dafiti.com.co+%22montgreen%22&sxsrf=ALiCzsa8Akr4UkhIxgH_iDwmd4phjRjCFA:1658619742888&ei=XofcYsnwNczrkvQP-ua-oAU&start=20&sa=N&ved=2ahUKEwjJl96EmJD5AhXMtYQIHXqzD1Q4ChDw0wN6BAgBEEU&biw=1536&bih=739&dpr=1.25',
            'https://www.google.com/search?q=site:dafiti.com.co+%22montgreen%22&sxsrf=ALiCzsZ_DMVQecELOofOac0vbeq-qDaEIA:1658619782616&ei=hofcYv6lJbyZwbkPlvaosAU&start=30&sa=N&ved=2ahUKEwj-gNeXmJD5AhW8TDABHRY7ClY4FBDw0wN6BAgBEEM&biw=1536&bih=739&dpr=1.25',

            ]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse )


    def parse(self, response):
        links = response.xpath('//div[@class="yuRUbf"]//a/@href').getall()
        print(links)

        for idx, link in enumerate(links):
            logger.info(f'Link {idx+1}/{len(links)}')
            if link:
                # link = 'http://localhost:8050/render.html?url={}'.format(link)
                yield response.follow(link, callback=self.new_parse, cb_kwargs={'link':link, 'idx':idx+1,'len':len(links)})


        # next_page = response.xpath('//li[@class="page-item next"]/a/@href').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def new_parse(self, response, **kwargs):

        title = ' '.join([i.capitalize() for i in response.xpath('//h3[@class="prd-title "]/text()').get().split(' ')])
        brand =  response.xpath('//h2[@class="prd-brand mbs"]/text()').get().capitalize()
        description =  remove_blank_spaces(' '.join(response.xpath('//*[@class="prd-information mbl prm"]//text()').getall()))
        
        try:
            sexo = response.xpath('//tr[contains(.,"Sexo")]/td[last()]/text()').get()
        except Exception as ex:
            sexo = None
        try:
            material_ext = response.xpath('//tr[contains(.,"Material exterior")]/td[last()]/text()').get()
        except Exception as ex:
            material_ext = None
        try:
            material_suela = response.xpath('//tr[contains(.,"Material exterior de suela")]/td[last()]/text()').get()
        except Exception as ex:
            material_suela = None
        try:
            color = response.xpath('//tr[contains(.,"Color")]/td[last()]/text()').get().capitalize()
        except Exception as ex:
            color = None
        try:
            description_short = remove_blank_spaces( response.xpath('//tr[contains(.,"Descripción corta")]/td[last()]/p/text()').get())
        except Exception as ex:
            description_short = None
        try:
            activity = response.xpath('//tr[contains(.,"Actividad")]/td[last()]//text()').get().capitalize()
        except Exception as ex:
            activity = None
        try:
            art_code = response.xpath('//tr[contains(.,"Código Artículo")]/td[last()]//text()').get()
        except Exception as ex:
            art_code = None

        url = kwargs['link']
        image = driver.get(url)
        time.sleep(3)
        image = driver.find_element_by_xpath('//div[@class="contProductZoom lfloat"]//img').get_attribute('data-zoom-image')
        # image = response.xpath('//div[@class="contProductZoom lfloat"]//img/@src').get()
        title_for_image = '_'.join(title.split(' '))
        # print(url)
        for i in range(0, 5):
            try:
                image = re.sub(r'\d-zoom','{}-zoom'.format(i+1),image)
                print('Image: ',image)  
                image_name, path_image = download_images.download(image,idx=i,len_links='5', nombre_del_lugar=title_for_image,main_dir_name='data_'+self.name)

            except Exception as e:
                pass
                # try:
                #     image_name, path_image =download_images.download_image_with_requests(image,idx=i,len_links='5', nombre_del_lugar=title_for_image,main_dir_name='data_'+self.name)
                # except Exception:
                #     pass

        yield{
            'Link': kwargs['link'],
            'Images Folder':path_image,
            'Brand':brand,
            'Product Title':title,
            'Detalles del Producto':description,
            'Sexo': sexo,
            'Material exterior':material_ext,
            'Material exterior de la suela':material_suela,
            'Color':color,
            'Description corta':description_short,
            'Actividad':activity,
            'Código Artículo':art_code ,
            'Image_name':image_name       }