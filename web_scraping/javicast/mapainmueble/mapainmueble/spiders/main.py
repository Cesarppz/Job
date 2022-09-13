import scrapy
from datetime import datetime

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

class GoogleComSpider(scrapy.Spider):
    name = 'mapainmueble'
    start_urls = [
        'https://mapainmueble.com/apartamentos-en-alquiler',
        'https://mapainmueble.com/casas-en-alquiler/',
        'https://mapainmueble.com/apartamentos-en-venta/',
        'https://mapainmueble.com/casas-en-venta-carretera-a-el-salvador/',
        'https://mapainmueble.com/casas-en-venta-san-cristobal/',
        'https://mapainmueble.com/casas-en-venta-en-zona-16/',
        'https://mapainmueble.com/casas-en-venta-muxbal/',
        'https://mapainmueble.com/casas-venta-antigua-guatemala/',
        'https://mapainmueble.com/casas-en-venta-zona-15/',
        'https://mapainmueble.com/casas-en-venta-zona-14/',
        'https://mapainmueble.com/casas-venta-zona-13/',
        'https://mapainmueble.com/casas-en-venta-zona-10/'

        ]

    custom_settings= {
                        'FEED_URI':f'results_{name}_{dia}_{mes}.csv',
                        'FEED_FORMAT':'csv'
                        }

    def parse(self, response):
        links = response.xpath('//h4/a/@href').getall()

        for link in links:
            yield response.follow(link, callback=self.second_parse)

        next_page =  response.xpath('//li[@class="roundright"]//a/@href').get()
        if next_page:
            yield response.follow(next_page, callback= self.parse)

    def get_info(self, response):
        try:
            x = response.get().strip()
            return x 
        except Exception:
            return None


    def second_parse(self, response):
        title = response.xpath('//h1/text()').get().strip()
        precio = self.get_info(response.xpath('//div/strong[contains(text(),"Precio:")]/../text()'))
        lote_size = self.get_info(response.xpath('//div/strong[contains(text(),"Tamaño del lote del Inmueble:")]/../text()'))
        property_size = self.get_info( response.xpath('//div/strong[contains(text(),"Tamaño de la propiedad:")]/../text()'))
        area = self.get_info( response.xpath('//div/strong[contains(text(),"Área:")]/../a/text()'))
        city = self.get_info(response.xpath('//div/strong[contains(text(),"Ciudad:")]/../a/text()'))
        rooms = self.get_info(response.xpath('//div/strong[contains(text(),"Dormitorios:")]/../text()'))
        bat = self.get_info(response.xpath('//div/strong[contains(text(),"Baños:")]/../text()'))
        parqueos = self.get_info(response.xpath('//div/strong[contains(text(),"Parqueos:")]/../text()'))
        id_propety = self.get_info(response.xpath('//div/strong[contains(text(),"ID de la propiedad:")]/../text()'))
        park = str(parqueos) + " / " + str(id_propety)
        modality = response.xpath('//div[@class="cat_n_type"]/div[@class="property_title_label"]/text()').get()
        type_inmueble = response.xpath('//div[@class="cat_n_type"]/div[@class="property_title_label actioncat"]/text()').get()


        yield{
            'Title': title,
            'Precio': precio,
            'Tamaño de la propiedad': property_size,
            'Tamaño del lote del inmueble': lote_size,
            'Área': area,
            'Ciudad': city,
            'Dormitorios': rooms,
            'Baños': bat,
            'Parqueos and ID de la propiedad': park,
            'Modalidad': modality,
            'Tipo': type_inmueble

        }
