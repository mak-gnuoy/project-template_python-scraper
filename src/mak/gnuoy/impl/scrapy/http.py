from typing import Any, Dict, Optional
import scrapy


class HTTPSpider(scrapy.Spider):
    name = "http"
    headers: Optional[Dict[str, Any]] = None
    callback = None

    def start_requests(self):
        for url in self.start_urls:
            return self.request(url, headers=self.headers)

    def request(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        if headers is None:
            headers = self.headers

        yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse)

    def parse(self, response):
        resp = {
            "url": response.url,
            "status": response.status,
            "headers": response.headers,
            "body": response.body,
            "protocol": response.protocol,
            "request": {
                "url": response.request.url,
                "method": response.request.method,
                "meta": response.request.meta,
                "body": response.request.body,
                "headers": response.request.headers,
            },
        }

        return self.callback(resp, self)  # type: ignore
