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
from agenda_tools import tools
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
pattern_link = re.compile(r'.*/no/bikes/?(\d+)*/(\w*)')


options = webdriver.FirefoxOptions()
options.add_argument('--private')
# options.add_argument('--no-sandbox')
# options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0')
driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

class MainSpider(scrapy.Spider):
    name = 'hard'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}

    def start_requests(self):
        urls = ['https://www.hardrocx.no/no/bikes/2019/electric',
                'https://www.hardrocx.no/no/bikes/2019/mountain-bikes',
                'https://www.hardrocx.no/no/bikes/2019/adventure',
                'https://www.hardrocx.no/no/bikes/2019/fatbike',
                'https://www.hardrocx.no/no/bikes/2019/hybrid',
                'https://www.hardrocx.no/no/bikes/2019/road',
                'https://www.hardrocx.no/no/bikes/2019/kids',
                'https://www.hardrocx.no/no/bikes/2019/lady',
                'https://www.hardrocx.no/no/bikes/2020/electric',
                'https://www.hardrocx.no/no/bikes/2020/mountain-bikes',
                'https://www.hardrocx.no/no/bikes/2020/adventure',
                'https://www.hardrocx.no/no/bikes/2020/fatbike',
                'https://www.hardrocx.no/no/bikes/2020/hybrid',
                'https://www.hardrocx.no/no/bikes/2020/road',
                'https://www.hardrocx.no/no/bikes/2020/kids',
                'https://www.hardrocx.no/no/bikes/2020/lady',
                'https://www.hardrocx.no/no/bikes/2021/electric',
                'https://www.hardrocx.no/no/bikes/2021/mountain-bikes',
                'https://www.hardrocx.no/no/bikes/2021/adventure',
                'https://www.hardrocx.no/no/bikes/2021/fatbike',
                'https://www.hardrocx.no/no/bikes/2021/hybrid',
                'https://www.hardrocx.no/no/bikes/2021/road',
                'https://www.hardrocx.no/no/bikes/2021/kids',
                'https://www.hardrocx.no/no/bikes/2021/lady'
                ]
        for url in urls:
            driver.get(url)
            time.sleep(5)
            category = re.match(pattern_link, url).group(2)
            year = re.match(pattern_link, url).group(1)
            links = tools.get_links_by_scralling(url, '//a[@class="bikes-list__item"]', driver=driver)
            print('Links: ',)
            #links = [i.get_attribute('href') for i in driver.find_elements_by_xpath('//a[@class="bikes-list__item"]')]
            for link in links:
                yield scrapy.Request(url=link, callback=self.parse, cb_kwargs={'category':category, 'year':year})



    # def parse(self, response, **kwargs):
    #     category = kwargs['category']
    #     driver.get(response.request.url)
    #     time.sleep(3)
    #     links  = [i.get_attribute('href') for i in driver.find_elements_by_xpath('//a[@class="bikes-list__item"]')]

    #     for link in links:

    #         yield response.follow(link, callback=self.second_parse, cb_kwargs={'link': link, 'category':category})

    #     # next_page = response.xpath('//a[@class="next page-link bg-secondary border-0 text-white"]/@href').get()
    #     # if next_page:
    #     #     yield response.follow(next_page, callback=self.parse)


    def extract_info(driver, xpath, attr='text'):
        try:
            element = driver.find_element_by_xpath(xpath)
            if attr == 'text':
                element = element.text
            else:
                element = element.get_attribute(attr)
        except:
            raise ValueError('Could not find element')
    
    def parse(self, response, **kwargs):
        link = response.request.url
        #brand
        driver.get(link)
        wait = WebDriverWait(driver, 60)
        image = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="carousel__item"]/img'))).get_attribute('src')
        brand = 'Hardrocx'
        Model =  driver.find_element_by_xpath('//div[@class="bike__details"]//h1').text
        year  = kwargs['year']
        # image = driver.find_element_by_xpath('//picture/img').get_attribute('src')
        #image =  response.xpath('//img[@data-toggle="lightbox"]/@src').get()
        image_title = '_'.join(Model.split(' ')).lower()+ str(random.randint(0,1000)).replace('/','').replace('\\','').replace('!','')
        print('Image: ', image)
        image_name  = download_images.download_image_with_requests(image, title_for_image=image_title, nombre_del_lugar='data'+self.name)
        try:
            price = driver.find_element_by_xpath('//span[@class="bike__details-price"]').text
        except:
            price = None
        category =  kwargs['category']
        try:
            wheels  = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Hjulsett")]//span[@class="copy"]').text
        except:
            wheels = None
        try:
            frame = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Ramme")]//span[@class="copy"]').text
        except:
            wheels = None
        try:
            suspension_fork =  driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Gaffel")]//span[@class="copy"]').text
        except:
            suspension_fork = None
        try:
            rear_derailleur = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Girstang")]//span[@class="copy"]').text 
        except:
            rear_derailleur = None
        try:
            shift_levers = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Girhendel")]//span[@class="copy"]').text
        except:
            shift_levers = None
        try:
            cassette = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Kassett")]//span[@class="copy"]').text
        except:
            cassette = None
        try:
            crank = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Krank")]//span[@class="copy"]').text
        except:
            crank = None
        try:
            bottom_bracket = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Bunnbrakett")]//span[@class="copy"]').text
        except:
            bottom_bracket = None
        try:
            chain = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Kjede")]//span[@class="copy"]').text
        except:
            chain = None
        try:
            pedals = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Pedaler")]//span[@class="copy"]').text
        except:
            pedals = None
        try:
            rims = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Felger")]//span[@class="copy"]').text
        except:
            rims = None 
        try:
            tires = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Antall gir")]//span[@class="copy"]').text
        except:
            tires = None
        try:
            brakes = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Bremser")]//span[@class="copy"]').text
        except:
            brakes = None
        try:
            stem = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Stilk")]//span[@class="copy"]').text
        except:
            stem = None
        try:
            handlebar = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Styre")]//span[@class="copy"]').text
        except:
            handlebar = None
        try:
            grips = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Grep")]//span[@class="copy"]').text
        except:
            grips = None 
        try:
            headset = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Headset")]//span[@class="copy"]').text
        except:
            headset = None 
        try:
            saddle = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Sadel")]//span[@class="copy"]').text
        except:
            saddle = None
        try:
            seatpost = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Sadelpinne")]//span[@class="copy"]').text
        except:
            seatpost = None
        try:
            motor =  driver.find_element_by_xpath('//table[@class="sc-89f09698-0 sc-89f09698-1 kQJYPE bicETb"]//tr[contains(.,"Motor")]/td').text
            e_bike = True
        except:
            motor = None
            e_bike = False
        try:
            battery =  driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Batteritype og kapasitet:")]//span[@class="copy"]').text
            e_bike = True
        except:
            battery = None
            e_bike = False
        try:
            charger = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Lader")]//span[@class="copy"]').text
        except:
            charger = None
        try:
            remote = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Fjernkontroll")]//span[@class="copy"]').text
        except:
            remote = None
        try:
            front_derailleur = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "frontgir")]//span[@class="copy"]').text
        except:
            front_derailleur = None
        try:
            chain_guide = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Kjedeføring")]//span[@class="copy"]').text
        except:
            chain_guide = None
        try:
            brake_levers = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "bremsehendel")]//span[@class="copy"]').text
        except:
            brake_levers = None
        try:
            rear_shock = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Bakdemper")]//span[@class="copy"]').text
        except:
            rear_shock = None
        try:
            disk_rotors = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Skiverotorer")]//span[@class="copy"]').text
        except:
            disk_rotors = None
        try:
            front_hub = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Fremre nav")]//span[@class="copy"]').text

        except :
            front_hub = None
        try:
            rear_hub = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "bakre nav")]//span[@class="copy"]').text
        except: 
            rear_hub = None
        try:
            spokes = driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Eiker")]//span[@class="copy"]').text
        except:
            spokes = None 
        try:
            chain_tensioner =  driver.find_element_by_xpath('//li[@class="bike__specs-item"][contains(., "Kjedestrammer")]//span[@class="copy"]').text
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
        

