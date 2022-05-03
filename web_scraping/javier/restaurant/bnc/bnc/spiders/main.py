import scrapy 
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from bnc.items import BncItem
import re
import time


class UserAgentSpider(scrapy.Spider):
    name = 'comida'
    # start_urls = [
    #    'https://www.bcnrestaurantes.com/restaurantes-barcelona.asp?lista=&start=&order='
    # ]

    def start_requests(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path='/home/cesar/Documents/job/web_scraping/javier/restaurant/chromedriver', options=options) 
        url = 'https://www.bcnrestaurantes.com/restaurantes-barcelona.asp?lista=&start=&order='
        driver.get(url)
        while True:
            try:
                driver.find_element_by_xpath('//*[contains(text(),"Ver más restaurantes ")]').click()
                list_restaurant  = driver.find_elements_by_xpath('//a[@class="list-group-item"]')
                for i in list_restaurant:
                    href = i.get_attribute('href')
                    #time.sleep(3)
                    yield scrapy.Request(href, callback=self.parse)
            except Exception as e:
               break



    def parse(self, response):
        title = response.xpath('//h3[@class="box-heading"]/text()').get()
        direccion = response.xpath('//span[@itemprop = "address"]//text()').getall()
        direccion = ' '.join(direccion).strip().replace('  ',' ')
        comida = response.xpath('//span[@itemprop = "servesCuisine"]/text()').get()
        valoracion = response.xpath('//div[@class="details-header-meta-actions"]/span[@class="label label-votes hidden-xs"]/text()').get()
        descuento = response.xpath('//ul[@id="tab_menu_cal"]/span/div[@class="text-primary"]/text()').get()
        category =  response.css('span.lista:nth-child(10)::text').get()
        telefono = response.xpath('//span[@itemprop="telephone"]/text()').get()
        rango_price = response.xpath('//span[@itemprop = "priceRange"]/text()').get()

        yield {
                        'Nombre lugar':title,
                        'Direccion':direccion,
                        'Valoracion':valoracion,
                        'Descuento':descuento,
                        'Categoria': category,
                        'Telefono':telefono,
                        'Comida':comida,
                        'Rango de precio':rango_price
                    }