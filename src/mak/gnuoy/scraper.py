from abc import abstractmethod
from typing import Any, Dict, Optional

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from mak.gnuoy.impl.scrapy.http import HTTPSpider
from mak.gnuoy.framework import Base


class Scraper(Base):
    def __init__(
        self,
        settings: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self._settings = settings
        self._logger.info(f"settings={self._settings}")

    @abstractmethod
    def scrape(self, config: Dict[str, Any]):
        pass


class ScrapyScraper(Scraper):
    def scrape(self, config: Dict[str, Any]):
        self._config = config
        self._logger.info(f"config={self._config}")

        process = CrawlerProcess(get_project_settings())
        HTTPSpider.custom_settings = self._settings
        HTTPSpider.start_urls = self._config["start_urls"]  # type: ignore
        HTTPSpider.headers = self._config["headers"]
        HTTPSpider.callback = self._received  # type: ignore
        process.crawl(HTTPSpider)

        if len(self._config["start_urls"]) > 1:
            self._logger.info(f"{self._config['start_urls']} are getting scraped.")
        else:
            self._logger.info(f"{self._config['start_urls']} is getting scraped.")
        process.start()
        if len(self._config["start_urls"]) > 1:
            self._logger.info(f"{self._config['start_urls']} scraping have done.")
        else:
            self._logger.info(f"{self._config['start_urls']} scraping has done.")

    def _received(
        self,
        response,
        client,
    ):
        self.client = client
        return self.received(response)

    @abstractmethod
    def received(self, response):
        pass
