import logging

from mak.gnuoy.framework import Config
from mak.gnuoy.scraper import ScrapyScraper

class ToScapeScraper(ScrapyScraper):

    def parse(self, request_url: str, response_status: int, response_headers: dict, response_body: str):
        self.logger.debug(f"name={self._name}")
        self.logger.debug(f"request_url={request_url}")
        self.logger.debug(f"response_status={response_status}")
        self.logger.debug(f"response_headers={response_headers}")
        self.logger.debug(f"response_body to 100 bytes={response_body.decode('utf-8')[:100]}")

if __name__ == '__main__':
    logging.getLogger().info("toscape scraper run")
    scraper = ToScapeScraper("toscape", Config.load("conf/toscrape.toml"))
    scraper.scrape()
    