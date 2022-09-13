
import pandas as pd
import requests
import os
import re 

from uuid import uuid4
from playwright.sync_api import sync_playwright  
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from agenda_tools import download_images
import logging


logger = logging.getLogger()

file_name_patter = re.compile(r'.*\.xlsx')
pattern_http = re.compile(r'https?://.*')

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
import requests


def loadbar(iteration,total,prefix='',suffix='',decimals=1,length=100,fill='>'):
   percent = ('{0:.' +str(decimals) + 'f}').format(100*(iteration/float(total)))
   filledLength = int(length * iteration // total)
   bar = fill * filledLength + '-' * (length - filledLength)
   print(f'\r{prefix} | {bar} | {percent}% {suffix}',end='\r')
   if iteration == total:
       print()


def start(file, names=['ID', 'URL']):
    df = pd.read_excel(file, header=1, names=names)
    # pdb.set_trace()

    df.drop_duplicates(inplace=True)

    images_df = list(df.loc[:, names[1]])

    list_names = list(df.loc[:, names[0]])

    return df, images_df, list_names


# "threading is for working in parallel, and async is for waiting in parallel".
def extract_images(img): 
    box_of_images = []
    for i in img:
        images = i.find_all('img')
        if images == []:
            continue
        box_of_images.extend(images)
    img = [i.get('src') for i in box_of_images]
    return img

#urls = range(1, 25000)

def start_playwright(url):
    with sync_playwright() as p:
        # print('Iniciando')
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page()
        page.goto(url)
        page.is_visible('img')
        html = page.inner_html('//body')
        img = extract_with_bs4(html)
        browser.close()

    return img

def start_requests(url):
    r = requests.get(url)
    # print('Making requests')
    try:
        img = extract_with_bs4(r.text)
        assert img != [], 'Lista vacia'
        return img, False
    except Exception as ex:
        return [], True


def extract_with_bs4(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        with open('atributos.txt', 'r', encoding='utf-8') as file:
            file_attr = file.readlines()
        
        for i in file_attr[1:]:
            data = i.split(';')
            name_tag = data[0].lower().strip()
            attr_class = data[1].lower().strip()
            attr_name = data[2]
            img = soup.find_all(name_tag, attrs={attr_class:attr_name})
            if img != []:
                break
        # img = soup.find_all('div', attrs={'class':"ficha_foto flex-image n item"})
        # if img == [] or img == None:
        #     img = soup.find_all('section', attrs={'class':'re-DetailMosaic re-DetailMosaic-grid5'})
    except Exception as ex:
        pass
    
    img = extract_images(img)
    return img


def extrac_info(url):
    try:
        img, js = start_requests(url)
        if js:
            img = start_playwright(url)
        
        if img == []:
            img = None
        assert img != None, 'Error al extrer la data'
    
    except AssertionError as ex:
        with open('info.log', 'a', encoding='utf-8') as file:
            file.write(f'\nError {ex} en la página: {url}')
    
    return img


def get_data(url,image_id, idx):
    imgs = extrac_info(url)  


    try:
        # os.system('clear')
        loadbar(idx, length_df, prefix='Progress:', suffix='Complete', length=100)
        for image in imgs:
            # print(image)
            title_for_image = image_id + str(uuid4())
            nombre_del_lugar = url.replace('/','_').replace('?','').replace('.','').replace('=','')
            
            if not re.match(pattern_http, image) :
                image = 'https:' + image
            
            try:
                download_images.download_image_with_requests(image,nombre_del_lugar=nombre_del_lugar,title_for_image=title_for_image, main_dir_name='data')
            except Exception as ax:
                with open('info.log', 'a', encoding='utf-8') as file:
                    file.write(f'\nError al descagar la imagen {ax} en la imágen: {image}')

    except Exception as ax:
        pass

def main(file):
    with ThreadPoolExecutor() as executor:
        df , urls, image_id = start(file)
        idx = range(0, int(df.shape[0]))
        global length_df
        length_df = df.shape[0]
        executor.map(get_data, urls, image_id, idx)

if __name__ == '__main__':
    files = os.listdir('files/')
    files = ['files/'+file for file in files if re.match(file_name_patter, file)]
    
    for file in files:
        main(file)


