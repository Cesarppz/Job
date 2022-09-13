from urllib import response
import scrapy
import logging
import re 
import time
import random

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
pattern_e = re.compile(r'https://mtbdatabase.com/e-bikes/.*')
from selenium import webdriver


options = webdriver.FirefoxOptions()
options.add_argument('--private')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0')
driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

class MainSpider(scrapy.Spider):
    name = 'mtb'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        url = 'https://mtbdatabase.com/bikes/'

        yield scrapy.Request(url=url, callback=self.parse )



    def parse(self, response):
        links = response.xpath('//div[@class="card border-0 bike-card square-card bike-card h-100"]/div[@class="card-body py-2 px-0"]/a/@href').getall()

        for link in links:

            yield response.follow(link, callback=self.second_parse, cb_kwargs={'link': link})

        next_page = response.xpath('//a[@class="next page-link bg-secondary border-0 text-white"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    
    def second_parse(self, response, **kwargs):
        driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

        link = kwargs['link']
        if re.match(pattern_e, response.request.url):
            e_bike = True 
        else:
            e_bike = False 
        #brand
        brand = response.xpath('//span[@class="crumbs text-muted"]/a[3]/text()').get()
        model =  response.xpath('//h1[@id="bike_name"]/text()').get()
        year  =  response.xpath('//div[@class="col-md-5 col-12"]/b/text()').get()
        driver.get(link)
        time.sleep(1)
        # wait = WebDriverWait(driver, 60)
        # image = wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@data-toggle="lightbox"]'))).get_attribute('src')
        image = driver.find_element_by_xpath('//img[@data-toggle="lightbox"]').get_attribute('src')
        driver.close()
        #image =  response.xpath('//img[@data-toggle="lightbox"]/@src').get()
        image_title = '_'.join(model.split(' ')).lower()+ str(random.randint(0,1000)).replace('/','')
        print('Image: ', image)
        image_name  = download_images.download_image_with_requests(image, title_for_image=image_title, nombre_del_lugar='data'+self.name)
        try:
            price = response.xpath('//div[@id="price_container"]/h4[@id="final_price"]/text()').get()
        except:
            price = None
        category =  response.xpath('//a[@class="badge badge-light rounded-0"]/text()').get()
        wheels  = response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Wheels")]//small[@class="text-muted"]/text()').get()
        frame = response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Frame")]//small[@class="text-muted"]/text()').get()
        suspension_fork = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Fork")]//small[@class="text-muted"]//text()').getall())
        rear_derailleur = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Rear Derailleur")]//small[@class="text-muted"]//text()').getall())
        shift_levers = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Shifters")]//small[@class="text-muted"]//text()').getall())
        try:
            cassette = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Cassette")]//small[@class="text-muted"]//text()').getall())
        except:
            cassette = None
        crank = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Crank")]//small[@class="text-muted"]//text()').getall())
        bottom_bracket =  ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Bottom Bracket")]//small[@class="text-muted"]//text()').getall())
        chain = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Chain")]//small[@class="text-muted"]//text()').getall())
        try:
            pedals = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Pedals")]//small[@class="text-muted"]//text()').getall())
        except:
            pedals = None
        try:
            rims = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Rims")]//small[@class="text-muted"]//text()').getall())
        except:
            rims = None 
        tires = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Tires")]//small[@class="text-muted"]//text()').getall())
        brakes = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Brakeset")]//small[@class="text-muted"]//text()').getall())
        stem = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Stem")]//small[@class="text-muted"]//text()').getall())
        handlebar = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Handlebar")]//small[@class="text-muted"]//text()').getall())
        try:
            grips = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Grips")]//small[@class="text-muted"]//text()').getall())
        except:
            grips = None 
        try:
            headset = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Headset")]//small[@class="text-muted"]//text()').getall())
        except:
            headset = None 
        saddle = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Saddle")]//small[@class="text-muted"]//text()').getall())
        seatpost = ' '.join(response.xpath('//li[@class=" list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Seatpost")]//small[@class="text-muted"]//text()').getall())
        try:
            motor =  ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Motor")]//small[@class="text-muted"]//text()').getall())
            if motor != None and motor != '':
                e_bike = True
        except:
            motor = None
            e_bike = False
        battery =  ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Battery")]//small[@class="text-muted"]//text()').getall())
        try:
            charger = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Charger")]//small[@class="text-muted"]//text()').getall())
        except:
            charger = None
        try:
            remote = None
        except:
            remote = None
        try:
            front_derailleur = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Front Derailleur")]//small[@class="text-muted"]//text()').getall())
        except:
            front_derailleur = None
        try:
            chain_guide = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Chain Guide")]//small[@class="text-muted"]//text()').getall())
        except:
            chain_guide = None
        try:
            brake_levers = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Brake Levers")]//small[@class="text-muted"]//text()').getall())
        except:
            brake_levers = None
        try:
            rear_shock = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Rear Shock")]//small[@class="text-muted"]//text()').getall())
        except:
            rear_shock = None
        try:
            disk_rotors = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Disk Rotors")]//small[@class="text-muted"]//text()').getall())
        except:
            disk_rotors = None
        try:
            front_hub = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Front Hub")]//small[@class="text-muted"]//text()').getall())
            try:
                front_hub = re.split('Rear:.*', front_hub)[0]
            except:
                pass
        except :
            front_hub = None
        try:
            rear_hub = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Rear Hub")]//small[@class="text-muted"]//text()').getall())
            try:
                rear_hub = re.split('Rear:', front_hub)[1]
            except:
                pass
        except: 
            rear_hub = None
        try:
            spokes = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Spokes")]//small[@class="text-muted"]//text()').getall())
        except:
            spokes = None 
        try:
            chain_tensioner =  ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0"][contains(.,"Chain Tensioner")]//small[@class="text-muted"]//text()').getall())
        except:
            chain_tensioner = None

        
        
        
        
        
        

        yield{
            'Link':link,
            'Electric':e_bike,
            'Brand':            remove_blank_spaces(brand),
            'Model':            remove_blank_spaces(model),
            'Year': year, 
            'Image': image_name,
            'Price': price,
            'Category':         self.function_to_remove_blank_spaces(category),
            'Wheels':           self.function_to_remove_blank_spaces( wheels),
            'Frame':            self.function_to_remove_blank_spaces( frame),
            'Suspension Fork':  self.function_to_remove_blank_spaces(suspension_fork),
            'Rear Derailleur':  self.function_to_remove_blank_spaces(rear_derailleur),
            'Shift Levers':     self.function_to_remove_blank_spaces(shift_levers),
            'Cassette':         self.function_to_remove_blank_spaces( cassette),
            'Crank':            self.function_to_remove_blank_spaces(crank),
            'Bottom Bracket':   self.function_to_remove_blank_spaces(bottom_bracket),
            'Chain':            self.function_to_remove_blank_spaces( chain),
            'Pedals':           self.function_to_remove_blank_spaces(pedals),
            'Rims':             self.function_to_remove_blank_spaces( rims),
            'Tires':            self.function_to_remove_blank_spaces( tires),
            'Brakes':           self.function_to_remove_blank_spaces( brakes),
            'Stem':             self.function_to_remove_blank_spaces( stem),
            'Handlebar':        self.function_to_remove_blank_spaces(handlebar),
            'Grips':            self.function_to_remove_blank_spaces(grips),
            'Headset':          self.function_to_remove_blank_spaces(headset),
            'Saddle':           self.function_to_remove_blank_spaces(saddle),
            'Seatpost':         self.function_to_remove_blank_spaces(seatpost),
            'Motor':            self.function_to_remove_blank_spaces( motor),
            'Battery':          self.function_to_remove_blank_spaces( battery),
            'Charger':          self.function_to_remove_blank_spaces( charger),
            'Remote':           self.function_to_remove_blank_spaces( remote),
            'Front Derailleur': self.function_to_remove_blank_spaces( front_derailleur),
            'Chain Guide':      self.function_to_remove_blank_spaces( chain_guide),
            'Brake Levers':     self.function_to_remove_blank_spaces( brake_levers),
            'Rear Shock':       self.function_to_remove_blank_spaces( rear_shock),
            'Disk Rotors':      self.function_to_remove_blank_spaces(disk_rotors),
            'Front Hub':        self.function_to_remove_blank_spaces( front_hub),
            'Rear Hub':         self.function_to_remove_blank_spaces( rear_hub),
            'Spokes':           self.function_to_remove_blank_spaces( spokes),
            'Chain Tensioner':  self.function_to_remove_blank_spaces(chain_tensioner)
        }
        
    
    def function_to_remove_blank_spaces(self, strings):
        if strings:
            return remove_blank_spaces(strings)
        return strings