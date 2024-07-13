import logging
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

from mak.gnuoy.framework import Config
from mak.gnuoy.scraper import ScrapyScraper

class ToScapeScraper(ScrapyScraper):

    def received(self, request_url: str, request_meta: dict, response_status: int, response_headers: dict, response_body: str, client):
        self.logger.debug(f"name={self._name}")
        self.logger.debug(f"request_url={request_url}")
        self.logger.debug(f"request_meta={request_meta}")
        self.logger.debug(f"response_status={response_status}")
        self.logger.debug(f"response_headers={response_headers}")
        self.logger.debug(f"response_body to 100 bytes={response_body.decode('utf-8')[:100]}")

        try:
            bs = BeautifulSoup(response_body, 'html.parser')
            href = bs.select("nav ul li.next a")[0].get("href")
            parsed_url = urlparse(request_url)
            next_url= urlunparse(parsed_url._replace(path = href))

            return client.request(url = next_url)
        except Exception as e:
            self.logger.debug(f"end of page : {request_url}\n{e}")

if __name__ == '__main__':
    logging.getLogger().info("toscape scraper run")
    scraper = ToScapeScraper("toscape", Config.load("conf/toscrape.toml"))
    scraper.scrape()