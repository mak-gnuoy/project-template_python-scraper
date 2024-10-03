from abc import abstractmethod
import os
from typing import Any, Dict, Optional

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from mak.gnuoy.impl.scrapy.http import HTTPSpider
from mak.gnuoy.framework import Base
from mak.gnuoy.store import JsonFileStore, Store


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

        os.makedirs(self._config["output"]["root_path"], exist_ok=True)

        self._root_output_path = os.path.join(
            self._config["output"]["root_path"], "scraped", self._config["name"]
        )
        os.makedirs(self._root_output_path, exist_ok=True)

        progress_store_filepath = os.path.join(self._root_output_path, f"progress.json")
        self._progress = JsonFileStore(progress_store_filepath)
        try:
            progress = self._progress.get("next_index_url")
            next_index_url = progress["next_index_url"]
            if next_index_url is None:
                self._logger.info(
                    f"Could not make a request with next_index_url={next_index_url}"
                )
                return
            else:
                self._logger.debug(f"next_index_url={next_index_url}")
        except (KeyError, FileNotFoundError) as e:
            next_index_url = self._config["start_url"]
            self._progress.set(**{"next_index_url": next_index_url})

        process = CrawlerProcess(get_project_settings())
        HTTPSpider.custom_settings = self._settings
        HTTPSpider.start_urls = [next_index_url]  # type: ignore
        HTTPSpider.headers = self._config["headers"]
        HTTPSpider.callback = self._received  # type: ignore
        process.crawl(HTTPSpider)

        self._logger.info(f"{self._config['name']} is getting scraped.")
        process.start()
        self._logger.info(f"{self._config['name']} scraping has done.")

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
