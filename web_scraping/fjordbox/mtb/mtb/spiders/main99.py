from tkinter import N
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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

logger = logging.getLogger(__name__)
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year
pattern_e = re.compile(r'https://mtbdatabase.com/e-bikes/.*')



options = webdriver.FirefoxOptions()
options.add_argument('--private')
# options.add_argument('--no-sandbox')
# options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0')
driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

class MainSpider(scrapy.Spider):
    name = '99'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        url = 'https://99spokes.com/en/bikes'
        driver.get(url)
        time.sleep(5)
        links = [i.get_attribute('href') for i in driver.find_elements('xpath','//div[@class="sc-89f09698-0 sc-89f09698-1 bvZPvD hpuEdD"]//a[@class="sc-d44587c2-0 sc-d44587c2-1 KUBfh iwfJdr"]')]
        print('Links: ',links)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse )



    def parse(self, response):
        driver.get(response.request.url)
        time.sleep(3)
        links  = [i.get_attribute('href') for i in driver.find_elements('xpath','//a[@class="sc-d44587c2-0 sc-d44587c2-1 KUBfh gYREv"]')]

        for link in links:

            yield response.follow(link, callback=self.second_parse, cb_kwargs={'link': link})

        # next_page = response.xpath('//a[@class="next page-link bg-secondary border-0 text-white"]/@href').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)


    def extract_info(driver, xpath, attr='text'):
        try:
            element = driver.find_element('xpath',xpath)   
            if attr == 'text':
                element = element.text
            else:
                element = element.get_attribute(attr)
        except:
            raise ValueError('Could not find element')
    
    def second_parse(self, response, **kwargs):
        link = kwargs['link']
        #brand
        driver.get(link)
        time.sleep(1)
        wait = WebDriverWait(driver, 60)
        image = wait.until(EC.visibility_of_element_located((By.XPATH, '//picture/img'))).get_attribute('src')
        brand = driver.find_element('xpath','//ul[@class="sc-89f09698-0 sc-89f09698-1 bvZPvD gvrfOq"]/li[position()=2]').text
        Model =  ' '.join(driver.find_element('xpath','//h1[@id="overview"]').text.split(' ')[1:])
        year  =  driver.find_element('xpath','//h1[@id="overview"]').text.split(' ')[0]    
        # image = driver.find_element('xpath','//picture/img').get_attribute('src')
        #image =  response.xpath('//img[@data-toggle="lightbox"]/@src').get()
        image_title = '_'.join(Model.split(' ')).lower()+ str(random.randint(0,1000)).replace('/','').replace('\\','').replace('!','')
        print('Image: ', image)
        image_name  = download_images.download_image_with_requests(image, title_for_image=image_title, nombre_del_lugar='data'+self.name)
        try:
            price = driver.find_element('xpath','//tr[contains(.,"RRP")]/td').text
        except:
            price = None
        category =  driver.find_element('xpath','//ul[@class="sc-89f09698-0 sc-89f09698-1 bvZPvD gvrfOq"]/li[position()=4]').text
        try:
            wheels  = driver.find_element('xpath','//tr[contains(.,"Wheels")]/td').text
        except:
            category = None
        frame = driver.find_element('xpath','//tr[contains(.,"Frame")]/td').text
        try:
            suspension_fork =  driver.find_element('xpath','//tr[contains(.,"Fork")]/td').text
        except:
            suspension_fork = None
        try:
            rear_derailleur = driver.find_element('xpath','//tr[contains(.,"Rear )Derailleur"]/td').text
        except:
            rear_derailleur = None
        try:
            shift_levers = driver.find_element('xpath','//tr[contains(.,"Shifters")]/td').text
        except:
            shift_levers = None
        try:
            cassette = driver.find_element('xpath','//tr[contains(.,"Cassette")]/td').text
        except:
            cassette = None
        try:
            crank = driver.find_element('xpath','//tr[contains(.,"Crank")]/td').text
        except:
            crank = None
        try:
            bottom_bracket =  driver.find_element('xpath','//th[text()="Bottom Bracket"]/../td').text
        except:
            bottom_bracket = None
        try:
            chain = driver.find_element('xpath','//th[text()="Chain"]/../td').text
        except:
            chain = None
        try:
            pedals = driver.find_element('xpath','//th[text()="Pedals"]/../td').text
        except:
            pedals = None
        try:
            rims = driver.find_element('xpath','//th[text()="Rims"]/../td').text
        except:
            rims = None 
        try:
            tires = driver.find_element('xpath','//th[text()="Tires"]/../td').text
        except:
            tires = None
        try:
            brakes = driver.find_element('xpath','//th[text()="Brakes"]/../td').text
        except:
            brakes = None
        try:
            stem = driver.find_element('xpath','//th[text()="Stem"]/../td').text
        except:
            stem = None
        try:
            handlebar = driver.find_element('xpath','//th[text()="Handlebar"]/../td').text
        except:
            handlebar = None
        try:
            grips = driver.find_element('xpath','//th[text()="Grips"]/../td').text
        except:
            grips = None 
        try:
            headset = driver.find_element('xpath','//th[text()="Headset"]/../td').text
        except:
            headset = None 
        try:
            saddle = driver.find_element('xpath','//th[text()="Saddle"]/../td').text
        except:
            saddle = None
        try:
            seatpost = driver.find_element('xpath','//th[text()="Seatpost"]/../td').text
        except:
            seatpost = None
        try:
            motor =  driver.find_element('xpath','//tr[contains(.,"Motor"))]/td').text
            e_bike = True
        except:
            motor = None
            e_bike = False
        try:
            battery =  driver.find_element('xpath','//tr[contains(.,"Battery"))]/td').text
        except:
            battery = None
        try:
            charger = ' '.join(response.xpath('//li[@class="list-group-item border-left-0 border-right-0 rounded-0[text()="Charger"]//small[@class="text-muted"]//text()').getall())
        except:
            charger = None
        try:
            remote = driver.find_element('xpath','//tr[contains(.,"Remote")]/td').text
        except:
            remote = None
        try:
            front_derailleur = driver.find_element('xpath','//th[text()="Front Derailleur"]/../td').text
        except:
            front_derailleur = None
        try:
            chain_guide = driver.find_element('xpath','//th[text()="Chain Guide"]/../td').text
        except:
            chain_guide = None
        try:
            brake_levers = driver.find_element('xpath','//th[text()="Brake Levers"]/../td').text
        except:
            brake_levers = None
        try:
            rear_shock = driver.find_element('xpath','//th[text()="Rear Shock"]/../td').text
        except:
            rear_shock = None
        try:
            disk_rotors = driver.find_element('xpath','//th[text()="Disk Rotors"]/../td').text
        except:
            disk_rotors = None
        try:
            front_hub = driver.find_element('xpath','//th[text()="Front Hub"]/../td').text

        except :
            front_hub = None
        try:
            rear_hub = driver.find_element('xpath','//th[text()="Rear Hub"]/../td').text
        except: 
            rear_hub = None
        try:
            spokes = driver.find_element('xpath','//table//th[text()="Spokes"]/../td').text
        except:
            spokes = None 
        try:
            chain_tensioner =  driver.find_element('xpath','//th[text()="Chain Tensioner"]/../td').text
        except:
            chain_tensioner = None

        
        
        
        
        
        

        yield{
            'Link':link,
            'Electric':e_bike,
            'Brand': brand,
            'Model': Model,
            'Year': year, 
            'Image': image_name,
            'Price': price,
            'Category': category,
            'Wheels': wheels,
            'Frame': frame,
            'Suspension Fork':suspension_fork,
            'Rear Derailleur':rear_derailleur,
            'Shift Levers':shift_levers,
            'Cassette': cassette,
            'Crank':crank,
            'Bottom Bracket':bottom_bracket,
            'Chain': chain,
            'Pedals':pedals,
            'Rims': rims,
            'Tires': tires,
            'Brakes': brakes,
            'Stem': stem,
            'Handlebar':handlebar,
            'Grips':grips,
            'Headset':headset,
            'Saddle':saddle,
            'Seatpost':seatpost,
            'Motor': motor,
            'Battery': battery,
            'Charger': charger,
            'Remote': remote,
            'Front Derailleur': front_derailleur,
            'Chain Guide': chain_guide,
            'Brake Levers': brake_levers,
            'Rear Shock': rear_shock,
            'Disk Rotors':disk_rotors,
            'Front Hub': front_hub,
            'Rear Hub': rear_hub,
            'Spokes': spokes,
            'Chain Tensioner':chain_tensioner
        }
        

