from abc import abstractmethod
from typing import Any, Dict, List, Optional

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from mak.gnuoy.impl.scrapy.http import HTTPSpider
from mak.gnuoy.framework import Base


class Scraper(Base):
    def __init__(
        self, config: Dict[str, Any], settings: Optional[Dict[str, Any]] = None
    ):
        super().__init__()

        self._logger.info(f"settings={settings}")
        self._logger.info(f"config={config}")
        self._name = config["name"]
        self._config = config
        self._settings = settings

    @abstractmethod
    def scrape(
        self, urls: Optional[List[str]] = None, headers: Optional[Dict[str, Any]] = None
    ):
        pass


class ScrapyScraper(Scraper):
    def scrape(
        self, urls: Optional[List[str]] = None, headers: Optional[Dict[str, Any]] = None
    ):
        if urls is None or len(urls) == 0:
            urls = self._config["start_urls"]
        if headers is None:
            headers = self._config["headers"]

        process = CrawlerProcess(get_project_settings())
        HTTPSpider.custom_settings = self._settings
        HTTPSpider.start_urls = urls  # type: ignore
        HTTPSpider.headers = headers
        HTTPSpider.callback = self._received  # type: ignore
        process.crawl(HTTPSpider)
        process.start()

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
