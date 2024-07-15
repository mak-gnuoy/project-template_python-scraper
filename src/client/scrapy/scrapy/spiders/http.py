import scrapy

class HTTPSpider(scrapy.Spider):
    name = "http"
    callback = None
    headers = None

    def start_requests(self):
        for url in self.start_urls:
            return self.request(url, headers = self.headers)

    def request(self, url: str, headers: dict = None, meta: dict = None):
        if headers is None:
            headers = self.headers
        
        yield scrapy.Request(
            url = url,
            headers = headers,
            meta = meta,
            callback = self.parse
        )

    def parse(self, response):
        if response.status == 200:        
            return self.callback(response.url, response.meta, response.status, response.headers, response.body, self)
