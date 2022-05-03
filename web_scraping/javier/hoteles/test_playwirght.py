import requests
import time
import pickle
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup


url_info_page = 'https://viajecaminodesantiago.com/camino-frances'
url = "https://www.booking.com/index.es.html?label=gen173nr-1DCAEoggI46AdIM1gEaPEBiAEBmAEKuAEZyAEP2AED6AEBiAIBqAIDuAKfic6RBsACAdICJGJmOWFhZmQ5LTYyMDUtNGRlMC05MTliLWFkNTY4MjI2ZjgwONgCBOACAQ;sid=d66a016dcaeb9f47c6acc13833910118;keep_landing=1&sb_price_type=total&"


def get_next_page(page):
    try:
        try:
            page.is_visible('//div[@data-testid="property-card"]')
        except:
            raise Exception(f"Error en la page {page.url}")
        time.sleep(5)
        page.locator("[aria-label=\"Página\\ siguiente\"]").click()
        return page
    except:
        pass
        

def get_boxes(html):
    soup = BeautifulSoup(html,'lxml')
    box = soup.find_all("div",attrs={'data-testid':"property-card"})
    links = [i.a.get('href') for i in box]
    # print(f'Elemntos : {links}')
    return links


def get_names():
    r = requests.get('https://viajecaminodesantiago.com/camino-frances')
    soup = BeautifulSoup(r.text, 'lxml')
    names = [j.strip() for i in soup.find_all('div',attrs={'class':"vcs_stage"}) for j in i.find('span',attrs={'class':"vcs_stage_title"})]
    return names

def get_info_for_page(page):
    page.wait_for_timeout(5000)
    links_pages = page.query_selector_all('//h3/a')
    for i in links_pages:
        with page.expect_popup() as popup_info:
            i.click()
            page1 = popup_info.value
            print(page1.query_selector('//h2').inner_text())
            page1.close()
    

    # habitaciones = page.query_selector('//tbody/tr/td[@class="hprt-table-cell -first hprt-table-cell-roomtype droom_seperator"]//div[@class="hprt-roomtype-block hprt-roomtype-name hp_rt_room_name_icon__container"]').text_content()
    # print('*'*5,habitaciones,'*'*5)


def get_main_pages(page):
    box_links = []
    names = get_names()
    for name in names:
        try:
            # Click [placeholder="¿Adónde\ vas\?"]
            page.locator("[placeholder=\"¿Adónde\\ vas\\?\"]").click()
            # Click [placeholder="¿Adónde\ vas\?"]

            page.locator("[placeholder=\"¿Adónde\\ vas\\?\"]").fill(name)
            # Press Enter
            page.locator("[placeholder=\"¿Adónde\\ vas\\?\"]").press("Enter")
            # assert page.url == "https://www.booking.com/searchresults.es.html?label=gen173nr-1BCAEoggI46AdIM1gEaPEBiAEBmAEKuAEZyAEP2AEB6AEBiAIBqAIDuAKfic6RBsACAdICJGJmOWFhZmQ5LTYyMDUtNGRlMC05MTliLWFkNTY4MjI2ZjgwONgCBeACAQ&lang=es&sid=cea79ae5214f90a13eba7734d501967b&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.es.html%3Flabel%3Dgen173nr-1BCAEoggI46AdIM1gEaPEBiAEBmAEKuAEZyAEP2AEB6AEBiAIBqAIDuAKfic6RBsACAdICJGJmOWFhZmQ5LTYyMDUtNGRlMC05MTliLWFkNTY4MjI2ZjgwONgCBeACAQ%3Bsid%3Dcea79ae5214f90a13eba7734d501967b%3Bsb_price_type%3Dtotal%26%3B&ss=Saint+Jean+Pied+de+Port+-+Roncesvalles&is_ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=Saint+Jean+Pied+de+Port+-+Roncesvalles&search_pageview_id=6aa48d451cc8025d"
            try:
                page.wait_for_selector('//div[@data-testid="property-card"]')
                get_info_for_page(page)
            except :
                raise Exception('Timepo agotado de espera')
                continue
            
            

            # while True:
            #     #print('Vuelta')
            #     resta = page.locator('//span[@class="_919e6c5ab"]').text_content().strip().replace('Mostrando','').split('-')
            #     # page.mouse.wheel(0,1000)
            #     #print(int(resta[-1].strip()) - int(resta[0].strip()))
            #     if int(resta[-1].strip()) - int(resta[0].strip()) >= 24:
            #         page = get_next_page(page)
            #         html = page.inner_html('//div[@id="basiclayout"]')
            #         box_links.append({'Name':name, 'Link':get_boxes(html)})
            #     else:
            #         #print('Acabo')
            #         html = page.inner_html('//div[@id="basiclayout"]')
            #         box_links.append({'Name':name, 'Link':get_boxes(html)})
            #         break
        
            page.goto(url)
        except Exception as ex:
            print(ex)
            pass
    
    #print(len(set()))
    #list_f = [i + '\n' for i in box_links]
    # with open('./list_of_links.dat','wb') as f:
    #     pickle.dump(box_links, f)
    # return box_links
    

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    # Go to https://www.booking.com/index.es.html?label=gen173nr-1DCAEoggI46AdIM1gEaPEBiAEBmAEKuAEZyAEP2AED6AEBiAIBqAIDuAKfic6RBsACAdICJGJmOWFhZmQ5LTYyMDUtNGRlMC05MTliLWFkNTY4MjI2ZjgwONgCBOACAQ;sid=d66a016dcaeb9f47c6acc13833910118;keep_landing=1&sb_price_type=total&
    page.goto(url)

    #Go for each of name pages
    get_main_pages(page)
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
