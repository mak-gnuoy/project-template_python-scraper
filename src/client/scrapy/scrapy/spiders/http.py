import scrapy

class HTTPSpider(scrapy.Spider):
    name = "http"
    callback = None

    def request(self, url: str):
        yield scrapy.Request(
            url = url,
            callback = self.parse
        )

    def parse(self, response):
        if response.status == 200:        
            return self.callback(response.url, response.status, response.headers, response.body, self)
