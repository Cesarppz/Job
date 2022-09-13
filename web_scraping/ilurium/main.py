from playwright.sync_api import sync_playwright  
from bs4 import BeautifulSoup
import requests_html
import pdb
from agenda_tools.tools import remove_blank_spaces
import time

def extract_with_bs4(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        with open('//mnt/c/Users/cesar/Documents/jobs/ilurium/atributos.txt', 'r', encoding='utf-8') as file:
            file_attr = file.readlines()
        
        for i in file_attr[1:]:
            data = i.split(';')
            name_tag = data[0].lower().strip()
            attr_class = data[1].lower().strip()
            attr_name = data[2].replace('\n', '')
            img = soup.find_all(name_tag, attrs={attr_class:attr_name})
            print(data)
            
            if img != []:
                print(img)
                break
    except Exception as ex:
        pass


url = 'https://www.idealista.com/98486221'
with sync_playwright() as p:
    print('Hola query_selector')
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    context = browser.new_context(
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    extra_http_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'},
)
# create a new page in a pristine context.
    page = context.new_page()
    page.goto(url)

    # time.sleep(2)
    page.wait_for_timeout(22000)
    if 'https://www.fotocasa.es' in url:
        try:
            page.wait_for_timeout(22000)
            page.wait_for_selector('//button[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center "]')
            # print(page.query_selector('//button[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center "]'))
            page.query_selector('//*[@data-testid="TcfAccept"]').click()
            page.query_selector('//div[@class="re-DetailMosaicPhoto-more"]').click()
            page.wait_for_timeout(2000)
        except Exception as ex:
            print(ex)
        
    html = page.inner_html('//body')
    # img = page.query_selector('//div[@class="flex-images n"]//img')

    extract_with_bs4(html)
    # soup = BeautifulSoup(html, 'html.parser')
    # # img = soup.find_all('ul', attrs={'class':"re-DetailMultimediaModal-listWrapper"})
    # img = soup.find_all('div', attrs={'class':'ficha_foto flex-image n item'})
    # box_of_images = []
    # for i in img:
    #     images = i.find_all('img')
    #     if images == []:
    #         continue
    #     box_of_images.extend(images)
    # img = [i.get('src') for i in box_of_images]
    # print(img)



