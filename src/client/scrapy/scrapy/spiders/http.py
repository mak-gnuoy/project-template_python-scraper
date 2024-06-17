import scrapy

class HTTPSpider(scrapy.Spider):
    name = "http"
    callback_func = None

    def parse(self, response):
        self.callback_func(response.url, response.status, response.headers, response.body)