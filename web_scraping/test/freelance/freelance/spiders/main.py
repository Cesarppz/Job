import scrapy


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
