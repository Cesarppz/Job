import scrapy


class Main5Spider(scrapy.Spider):
    name = 'main5'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def parse(self, response):
        pass
