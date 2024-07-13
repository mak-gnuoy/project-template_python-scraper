import scrapy

class HTTPSpider(scrapy.Spider):
    name = "http"
    callback = None

    def request(self, url: str, meta: dict = None):
        yield scrapy.Request(
            url = url,
            callback = self.parse,
            meta = meta
        )

    def parse(self, response):
        if response.status == 200:        
            return self.callback(response.url, response.meta, response.status, response.headers, response.body, self)
