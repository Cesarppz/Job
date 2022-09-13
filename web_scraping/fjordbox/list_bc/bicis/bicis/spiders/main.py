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

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver

logger = logging.getLogger(__name__)
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year
pattern_e = re.compile(r'https://mtbdatabase.com/e-bikes/.*')



# options = webdriver.FirefoxOptions()
# options.add_argument('--private')
# options.add_argument('--no-sandbox')
# options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0')
# driver = webdriver.Firefox(executable_path='/home/cesarppz/Documents/jobs/web_scraping/javier/agenda/driver/geckodriver', options=options)

class MainSpider(scrapy.Spider):
    name = 'list'
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8'}


    start_urls = ['https://hardrocx.no/no']

    def parse(self, response):
        # driver.get(response.request.url)
        # time.sleep(3)
        links  = response.xpath('//ul[@class="typeListSmall"]/li/a[position()=1]/@href').getall()

        for link in links:
            # print('Link : ',link)
            yield response.follow(link, callback=self.s_parse)
        # next_page = response.xpath('//a[@class="next page-link bg-secondary border-0 text-white"]/@href').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
    def s_parse(self, response):
        links = response.xpath('//span/a[@class="add"][position()=2]/@href').getall()
        
        if links == []:
            print('Entro',' -*- '*5)
            a = response.xpath('//div[@class="box2"]//a/@href').getall() 
            for i in a:
                # print('I; ', i)
                yield response.follow(i, callback=self.t_parse)
        
        for link in links:
            yield response.follow(link, callback=self.s_parse)

    
    def t_parse(self,response):
        links = response.xpath('//div[@class="box2"]//a/@href').getall() 
        for i in links:
            yield response.follow(i, callback=self.second_parse)

    
    def second_parse(self, response):
        link = response.request.url
        image = 'https://thebikelist.co.uk' + response.xpath('//a[@rel="bike"]/img/@src').get()
        # print('\nImage: ',image , ' - ', link)

        brand = response.xpath('//ol[@class="breadcrumbs"]/li[@itemprop="itemListElement"][position()=2]//span/text()').get()
        Model =  response.xpath('//*[@class="box2"]/h2/text()').get()
        year  =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Years")]//td/text()').get())
        image_title = '_'.join(Model.split(' ')).lower()+ str(random.randint(0,1000)).replace('/','').replace('\\','').replace('!','')
        # print('Image: ', image)
        image_name  = download_images.download_image_with_requests(image, title_for_image=image_title, nombre_del_lugar='data'+self.name)
        try:
            price = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"RRP")]//td/text()').get())
        except:
            price = None
        category =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Type")]//td/text()').get())
        wheels  = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Wheels")]//td/text()').get())
        frame =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Frame type")]//td/text()').get())
        try:
            suspension_fork =   remove_blank_spaces(' | '.join(response.xpath('//*[@class="spec"]//tr[contains(.,"Forks")]//td/text()').getall()))
        except:
            suspension_fork = None
        try:
            rear_derailleur = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Rear Derailleur")]//td/text()').get())
        except:
            rear_derailleur = None
        try:
            shift_levers = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Tires")]//td/text()').get())
        except:
            shift_levers = None
        try:
            cassette = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Cassette")]//td/text()').get())
        except:
            cassette = None
        try:
            crank = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Crank")]//td/text()').get())
        except:
            crank = None
        try:
            bottom_bracket = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Bottom Bracket")]//td/text()').get())
        except:
            bottom_bracket = None
        try:
            chain = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Chainset type")]//td/text()').get())
        except:
            chain = None
        try:
            pedals = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Pedals")]//td/text()').get())
        except:
            pedals = None
        try:
            rims = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Rims")]//td/text()').get())
        except:
            rims = None 
        try:
            tires =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Tyres")]//td/text()').get())
        except:
            tires = None
        try:
            brakes = remove_blank_spaces(' | '.join(response.xpath('//*[@class="spec"]//tr[contains(.,"Brake")]//td/text()').getall())).replace('  ','').replace('\r','')
        except:
            brakes = None
        try:
            stem = response.xpath('//*[@class="spec"]//tr[contains(.,"Stem")]//td/text()').get()
        except:
            stem = None
        try:
            handlebar = response.xpath('//*[@class="spec"]//tr[contains(.,"Handlebar")]//td/text()').get()
        except:
            handlebar = None
        try:
            grips = response.xpath('//*[@class="spec"]//tr[contains(.,"Grips")]//td/text()').get()
        except:
            grips = None 
        try:
            headset =  response.xpath('//*[@class="spec"]//tr[contains(.,"Headset")]//td/text()').get()
        except:
            headset = None 
        try:
            saddle = response.xpath('//*[@class="spec"]//tr[contains(.,"Saddle")]//td/text()').get()
        except:
            saddle = None
        try:
            seatpost = response.xpath('//*[@class="spec"]//tr[contains(.,"Seatpost")]//td/text()').get()
        except:
            seatpost = None
        try:
            motor =   response.xpath('//*[@class="spec"]//tr[contains(.,"Motor")]//td/text()').get()
            e_bike = True
        except:
            motor = None
            e_bike = False
        try:
            battery =  response.xpath('//*[@class="spec"]//tr[contains(.,"Battery")]//td/text()').get()
        except:
            battery = None
        try:
            charger =  response.xpath('//*[@class="spec"]//tr[contains(.,"Charger")]//td/text()').get()
        except:
            charger = None
        try:
            remote = response.xpath('//*[@class="spec"]//tr[contains(.,"Remote")]//td/text()').get()
        except:
            remote = None
        try:
            front_derailleur =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Front Derailleur")]//td/text()').get())
        except:
            front_derailleur = None
        try:
            chain_guide =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Chain Guide")]//td/text()').get())
        except:
            chain_guide = None
        try:
            brake_levers =  remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Brake Levers")]//td/text()').get())
        except:
            brake_levers = None
        try:
            rear_shock = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Rear Schock")]//td/text()').get())
        except:
            rear_shock = None
        try:
            disk_rotors = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Disk Rotors")]//td/text()').get())
        except:
            disk_rotors = None
        try:
            front_hub = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Hub Front")]//td/text()').get())

        except :
            front_hub = None
        try:
            rear_hub = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Hub Rear")]//td/text()').get())
        except: 
            rear_hub = None
        try:
            spokes = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Spokes")]//td/text()').get())
        except:
            spokes = None 
        try:
            chain_tensioner = remove_blank_spaces( response.xpath('//*[@class="spec"]//tr[contains(.,"Chain tensioner")]//td/text()').get())
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
        

