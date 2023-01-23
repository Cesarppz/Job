import scrapy 
import pickle 
import re
import datetime as dt
from datetime import datetime
import logging
import time
import pandas as pd

from scrapy_playwright.page import PageMethod, PageCoroutine
from agenda_tools.tools import remove_blank_spaces
from helper import should_abort_request

logger = logging.getLogger()
mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

pattern_schedule = re.compile(r'\d+\s+de\s+\w+')
pattern_horario = re.compile(r'([A-Za-záéíóú]+ \d+ de [A-Za-záéíóú]+)( y \d+ de [A-Za-záéíóú]+)?( a las \d+:\d+)?')


def extract_item(response_xpath):
        try:
            item = response_xpath
        except Exception:
            item = None

        return item

class Webscrape(scrapy.Spider):
    name = 'infocif'
    #allowed_domains = ['www.cinescallao.es']
    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv',
                        'FEED_EXPORT_ENCODING':'utf-8', 
                        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '300000',
                        'PLAYWRIGHT_ABORT_REQUEST': should_abort_request
                        }

    def start_requests(self):
        with open('/home/cesarppz/Documents/jobs/web_scraping/iworketing/ranking_infocif', 'rb') as file:
            links = pickle.load(file)

        df = []
        for i in links:
            df.append(pd.DataFrame(i))
        df = pd.concat(df)

        for link in df.values:
            link = link[-1]
            print(link)
            yield scrapy.Request(
                link, 
                callback=self.parse,
                meta = {
                    "playwright":True,
                    # "playwright_include_page": True,
                    "playwrite_page_methods":[
                        # PageMethod("wait_for_selector", 'text="EBITDA"'),
                        # PageMethod("evaluate", "window.scrollBy(0,document.body.scrollHeight)"),
                        PageCoroutine('waitForNavigation'),
                        # PageMethod("wait_for_selector", "#divbalances"),
                        # PageMethod("evaluate", "window.scrollBy(0,document.body.scrollHeight)"),

                        PageMethod("wait_for_selector", "#fe-informacion-izq")
                        # PageMethod("evaluate", "window.scrollBy(0,document.body.scrollHeight)")
                    ]
                }

            )

    


    def parse(self, response):
        cif = extract_item( response.xpath('//strong[contains(.,"CIF")]/following::h2[position()=1]/text()').get())
        domicilio = extract_item(remove_blank_spaces(''.join(response.xpath('//strong[contains(.,"Domicilio")]/following::p[position()=1]/text()').getall())))
        company_name = extract_item(response.xpath('//h1/text()').get())
        seniority = extract_item( remove_blank_spaces(response.xpath('//div[@id="fe-informacion-izq"]/strong[contains(text(),"Antigüedad")]/following::p/text()').get()))
        phone = extract_item(remove_blank_spaces(response.xpath('//div[@id="fe-informacion-izq"]/strong[contains(text(),"Teléfono")]/following::p/text()').get()))
        web = extract_item(remove_blank_spaces(response.xpath('//div[@id="fe-informacion-izq"]/strong[contains(text(),"Web")]/following::p/a/text()').get()))
        number_of_employees = extract_item( remove_blank_spaces(response.xpath('//strong[contains(text(),"Nº de empleados")]/following::p/text()').get()))
        ranking_number = extract_item(remove_blank_spaces(response.xpath('//div[@class="fl hoverred pr5 fs18"]/span/text()').get()))
        cuentas_anueales_years = extract_item( response.xpath('//tr[contains(., "Ingresos")]/td[@class="noborder "]').get())
        # income =  


        yield {
        'Cif':cif,
        'Domicilio':domicilio,
        'Nombre de Empresa':company_name,
        'Antiguedad':seniority,
        'Phone':phone,
        'Web':web,
        'Numero de empleados':number_of_employees,
        'ranking_number':ranking_number,
        'Año cuentas anuales':cuentas_anueales_years,
        # 'Ingresos':income,
        # 'Tendencia Ingresos':trend,
        # 'Resultados de explotación':operating_results,
        # 'Tendencia resultados de explotación':operating_trend,
        # 'net_worth':net_worth,
        # 'Beneficio Neto':gross_margin,
        # 'Tendencia Beneficio Neto':gross_margin_trend,
        # 'Deuda': debt,
        # 'Ros':ros,
        # 'Ros Tendencia':roe_trend,
        # 'Roe':roe_trend,
        # 'Roe Tendencia':roe_trend,
        # 'Liquidez':liquidity,
        # 'Liquidez Tendencia':liquidity_trend,
        # 'Solvencia':solvency,
        # 'Solvencia Tendencia':solvency_trend,
        # 'Matriz':matriz,
        # 'Patricipadas_matriz':patricipadas_matriz,
        # 'Cargos':cargos,
        # 'Analisis_taya_year':analisis_taya_year, 
        # 'Gastos_personal':gastos_personal,
        # 'Otros_gastos_explotacion':otros_gastos_explotacion
        
    }