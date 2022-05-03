from selenium import webdriver
import re
import time
import pandas as pd
import urllib
import subprocess
from agenda_tools import get_schedule, get_category, download_images, get_category, months
from datetime import datetime
import requests
from bs4 import BeautifulSoup
pattern = re.compile(r'[A-Za-záéíóú]+ (\d+/\d+, \d+:\d+h)')
day = datetime.now().day
mes = datetime.now().month
url = 'https://www.salagalileogalilei.com/agenda.php'

def get_driver():

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='./driver/geckodriver', options=options)
    driver.get(url)
    
    return driver


def category_transform(category):
    if category == 'Flamenco Fusión':
        category = 'Flamenco'
    elif category == 'Swing':
        category = 'Jazz y Soul'
    elif category == 'Jazz':
        category = 'Jazz y Soul'
    elif category == 'Canción de Autor':
        category = 'Música'
    elif category == 'Humor':
        category = 'Humor, Magia y Circo'
    elif category == 'Pop':
        category = 'Música'
    elif category == 'Rock':
        category = 'Música'
    elif category == 'Fusión':
        category = 'Música'
    elif category == 'Copla':
        category = 'Música'
    elif category == 'Pop-Rock':
        category = 'Música'
    elif category == 'Folk Rock':
        category = 'Música'
    elif category == 'Magia':
        category = 'Humor, Magia y Circo'
    elif category == 'Músicas del mundo':
        category = 'Música'
    elif category == 'Rock Familiar':
        category = 'Música'
    elif category == 'Magia Familiar':
        category = 'Humor, Magia y Circo'
    elif category == 'Música Cubana':
        category = 'Música'
    elif category == 'Flamenco-Percusión':
        category = 'Flamenco'
    elif category == 'Blues':
        category = 'Música'
    elif category == 'Coral':
        category = 'Música'
    elif category == 'Folk':
        category = 'Música'
    elif category == 'Gospel':
        category = 'Música'
    
    return category


def process(clicks, driver):
    data = []
    remove_from_list = []
    for idx, i in enumerate(clicks):
        #Abrir la ventana
        try:
            i.click()
            time.sleep(2)
            title = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[1]/div/span[@class="h2"]').text
            description = driver.find_element_by_xpath('//*[@class="highslide-wrapper dark"]/div/div/div/div').text
            all_schedule = driver.find_element_by_xpath('//*[@class="highslide-wrapper dark"]/div/div/div').text
            schedule, horario = re.findall(pattern,all_schedule)[0].split(',')
            img = driver.find_element_by_xpath('//*[@class="highslide-caption"]/img').get_attribute('src')

            time.sleep(2)
            driver.find_element_by_xpath('//img[@title="Click to close image, click and drag to move. Use arrow keys for next and previous."]').click()

            # process 
            #images_name = download_images.download(img,nombre_del_lugar='galileo_galilei',idx=idx+1,len_links=len(clicks))
            #Schedule
            dt = datetime.strptime(schedule,'%d/%m')
            from_to = datetime.strftime(dt,'%d/%m/%Y')
            #schedule
            schedule = datetime.strftime(dt,'%d %b').strip()
            schedule = get_schedule.transform_to_adv_eng_spa(schedule)
            

            data_dict = {
                'From':from_to,
                'To':from_to,
                'Desde':schedule.strip(),
                'Hasta':schedule.strip(),
                'Product_name':title,
                'Nombre_lugar':'Teatro Galileo Galilei',
                'Categoria':None,
                'Sub_categoria':None,
                'image':None,
                'Horario':horario,
                'Descripcion':description,
                'Area': 'Chamberi ',
                'Cuidad': 'Madrid',
                'Provincia': 'Madrid',
                'Country':'España',
                'Link':'https://www.salagalileogalilei.com/agenda.php'
            }
            print('Scraping ...')
            data.append(data_dict)
        except Exception as ex:
            print(ex)
            print(f'Error en el indice {idx}')
            remove_from_list.append(idx)

    return data, remove_from_list


def scraped_images(driver,remove_list):
    image_box_tail = []
    image_box_head = []

    for i in driver.find_elements_by_xpath('//div[@class="img-domingo"]/a/img'):
        link = i.get_attribute('src')
        image_box_tail.append(link)

    for i in driver.find_elements_by_xpath('//div[@class="img-shadow2"]/a/img'):
        link = i.get_attribute('src')
        image_box_head.append(link)

    images = image_box_head + image_box_tail
    images_names = []  
    for idx, img in enumerate(images):
        image_name = download_images.download(img,nombre_del_lugar='galileo_galilei',idx=idx+1,len_links=len(images))
        images_names.append(image_name)

    for i in remove_list:
        images_names.pop(i)
    
    return images_names


def scraped_category(driver, remove_list):
    category_box_tail = []
    category_box_head = []

    for i in driver.find_elements_by_xpath('//div[@class="img-domingo"]/span'):
        if i.text == '':
            category_box_tail.append('None')
        else:
            i = category_transform(i.text)
            category_box_tail.append(i)

    for i in driver.find_elements_by_xpath('//div[@class="img-shadow2"]/span'):
        if i.text == '' or i.text == None:
            category_box_head.append('None')
        else:
            i = category_transform(i.text)
            category_box_head.append(i)

    category = category_box_head + category_box_tail

    for i in remove_list:
        category.pop(i)

    return category


def scraped_id_category(category):
    id_box = []
    for i in category:
        if i == 'None':
            id_box.append('None')
        else :
            id_category = get_category.id_category(i)
            id_box.append(id_category)

    return id_box


def make_df(data,category,id_category,images):
    for idx, i in enumerate(data):
        n = 0
        try:
            data[idx] = pd.DataFrame(i)
        except ValueError as e:
            data[idx] = pd.DataFrame.from_dict(i,orient='index').transpose()


    df = pd.concat(data)

    df.drop_duplicates(inplace=True)

    df['Categoria'] = category

    df['Sub_categoria'] = id_category

    df['image'] = images

    return df


def write_df(df):
    df.to_csv('results_galileo_galilei_{}_{}.csv'.format(day,mes), index=False)


def main():
    driver = get_driver()
    clicks = driver.find_elements_by_xpath('//div[@class="img-shadow2"]/a/img')
    clicks2 = driver.find_elements_by_xpath('//div[@class="img-domingo"]/a/img')
    clicks = clicks + clicks2
    #print(clicks)
    if driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/a[1]/b'):
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/a[1]/b').click()
    data, remove_from_list = process(clicks, driver)
    images = scraped_images(driver, remove_list = remove_from_list)
    category = scraped_category(driver, remove_list = remove_from_list)
    id_category = scraped_id_category(category)
    df = make_df(data,category,id_category,images)
    write_df(df)
    driver.close()

if __name__ == '__main__':
    main()
