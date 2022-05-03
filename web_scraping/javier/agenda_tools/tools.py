from selenium import webdriver
from agenda_tools import get_schedule, get_category, download_images
import time 

def get_links_by_scralling(url,xpath_expresion, attribute='href',executable_path='../driver/geckodriver'):
    #Instanciar el navegador
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Firefox(executable_path='../driver/geckodriver', options=options)
    driver.get(url)
    #Get links scralling
    box = []
    previous_heigth = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)
        new_heigth = driver.execute_script('return document.body.scrollHeight')
        if new_heigth == previous_heigth:
            box.extend(driver.find_elements_by_xpath(xpath_expresion))
            break
        previous_heigth = new_heigth
    if attribute != 'text':
        box = [i.get_attribute(attribute) for i in box[1:]]
    else:
        box = [i.text for i in box[1:]]
    driver.close()
    return box


def get_headers(from_date,to_date,title,category,image_name,horario,link,description,place_name,latitud,longitud):
    id_category = get_category.id_category(category)
    main_category = get_category.main_category(category)

    return {
                'From':from_date,
                'To':to_date,
                # 'Desde': desde,
                # 'Hasta': hasta,
                'title/Product_name': title,
                'Place_name/address':place_name,
                'Categoria' : category,
                'Title_category':main_category,
                'Nº Category': id_category,
                'image':image_name,
                'Hours':horario,
                'Link_to_buy': link,
                'Description':description,
                #'Area': 'La Latina ',
                'City': 'Madrid',
                'Province': 'Madrid',
                'Country':'España',
                'latitud':latitud,
                'longitud':longitud,  
                'Link':link
                
                }



def get_attribute_by_selenium(url,xpath_expresion,text=True,list_number=0,attr='text'):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path='../driver/geckodriver', options=options)
    driver.get(url)
    time.sleep(0.5)
    if list_number == 1:
        result = driver.find_elements_by_xpath(xpath_expresion)
        result = ' '.join([i.text for i in result if i != ''])
        driver.close()
        return result
    elif list_number == 0:
        if attr == 'text':
            result = driver.find_elements_by_xpath(xpath_expresion).text
        else:
            result = driver.find_element_by_xpath(xpath_expresion).get_attribute(attr)
        driver.close()
        return result
    driver.close()


def remove_blank_spaces(text):
    return text.replace('\xa0',' ').replace('\n',' ').replace('\t',' ').replace('  ',' ').replace('\n',' ').strip()


# def get_links_by_scralling(self,url,xpath_expresion, attribute='href'):
#         #Instanciar el navegador
#         options = webdriver.FirefoxOptions()
#         options.add_argument("--headless")
#         #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#         driver = webdriver.Firefox(executable_path='../driver/geckodriver', options=options)
#         driver.get(url)
    

#         #Get links scralling
#         box = []
#         previous_heigth = driver.execute_script('return document.body.scrollHeight')
#         while True:
#             driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
#             time.sleep(5)
#             new_heigth = driver.execute_script('return document.body.scrollHeight')
#             if new_heigth == previous_heigth:
#                 box.extend(driver.find_elements_by_xpath(xpath_expresion))
#                 break
#             previous_heigth = new_heigth
#         box = [i.get_attribute(attribute) for i in box[1:]]
#         driver.close()
#         return box