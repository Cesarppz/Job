from selenium import webdriver
import pickle
import re 
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path  = '/home/cesar/Documents/job/web_scraping/javier/hoteles/list_of_links.dat'



def inizialize():
    options = webdriver.FirefoxOptions()
    options.add_argument('--private')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0')
    #options.add_argument("--headless")
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path='/home/cesar/Documents/job/web_scraping/javier/agenda/driver/geckodriver', options=options)
    return driver


def get_info(link,driver,city):
    info_by_link = []
    driver.get(link)
    time.sleep(3)

    try:
        #title 
        try:
            title =  WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//h2[@id="hp_hotel_name"]'))
                        ).text
        except:
            raise Exception("Tiempo agotado")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        #Habitaciones
        xpath_habitaciones = '//div[@class="_e3ed6b426 _425b57dc7 d79b273389 _b7ed60b59"]/div[@class="_361c04b9c _729127938 _78cd05546"]//div[@class="_a11e76d75 c5cf92dd20"]'
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_habitaciones)))
            habitaciones = [i.text for i in driver.find_elements_by_xpath('//div[@class="_e3ed6b426 _425b57dc7 d79b273389 _b7ed60b59"]/div[@class="_361c04b9c _729127938 _78cd05546"]//div[@class="_a11e76d75 c5cf92dd20"]')]
        except:
            raise Exception('No se encuentra habiatciones')
        
        if habitaciones == []:
            habitaciones = None
        
        #Services
        servicios = '  /  '.join([i.text.replace('\n',' - ') for i in driver.find_elements_by_xpath('//section[@id="hp_facilities_box"]//div[@class="hotel-facilities__list"]//div[@class="bui-spacer--large"]')])
        if servicios == []:
            servicios = None
        
        #Capcidad
        capacidad = [i.get_attribute('aria-label') for i in driver.find_elements_by_xpath('//div[@class="_361c04b9c _729127938 _10eb43c0c"]//div[@class="cea9cafb89"]')]
        if capacidad == []:
            capacidad = None
        #print(f'{capacidad}')
        #Location
        location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="\nhp_address_subtitle\njs-hp_address_subtitle\njq_tooltip\n"]'))).text        
        #Description
        try:
            # = driver.find_element_by_xpath('//div[@class="hp_desc_main_content"]').text.replace('\n','')
            description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="hp_desc_main_content"]'))).text.replace('\n','')
        except:
            try:
                description = driver.find_element_by_xpath('//div[@class="hp-description"]').text.replace('\n','')
            except:
                raise Exception(f"No hay descripcion {link}")

        #Images
        images = [i.get_attribute('src') for i in driver.find_elements_by_xpath('//div[@aria-hidden="true"]/a//img')][0]   
        
        for idx, habitacion in enumerate(habitaciones):
            info_by_link.append(
            {
                'Title':title,
                'Habitaciones':habitacion,
                'Services':servicios,
                'Capacidad':capacidad[idx],
                'Location':location,
                'Image':images,
                'City': city,
                'Description':description
            }
            #dict(Title=title,Habitaciones=habitaciones,Services=servicios,Capcidad=capacidad,Location=location,Iamges=iamges,City=city,Description=description)
        ) 
        return info_by_link

    except Exception as ex:
        print(ex)
        pass


def save_data(data):
    for idx, i in enumerate(data):
        try:
            data[idx] = pd.DataFrame(i)
        except ValueError as e:
            data[idx] = pd.DataFrame.from_dict(i,orient='index').transpose()
    
    data = pd.concat(data)
    #data.drop_duplicates(inplace=True)
    print(data.head())
    data.to_csv('hoteles_data.xlsx')


def run():
    #load
    data_list = []
    with open(path,'rb') as f:
        urls = pickle.load(f)

    driver = inizialize()

    for idx_u , url in enumerate(urls):
        print(f'Scraping {idx_u+1}/{len(urls)}')
        for i in url['Link']:
            data = get_info(i,driver,url['Name'])
            if data:
                data_list.extend(data)
    driver.close()
    with open('./data_info.dat','wb') as f:
        pickle.dump(data_list,f)
    save_data(data_list)
    print(data_list)


if __name__ == '__main__':
    run()