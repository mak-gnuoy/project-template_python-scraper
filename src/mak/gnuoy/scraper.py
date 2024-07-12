from abc import abstractmethod
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from client.scrapy.scrapy.spiders.http import HTTPSpider
from mak.gnuoy.framework import Config, Scraper

logging.getLogger('scrapy').propagate = False
logging.getLogger().propagate = False

class ScrapyScraper(Scraper):
    def scrape(self, url: str = None):
        super().scrape(url)

        process = CrawlerProcess(get_project_settings() )
        HTTPSpider.custom_settings = {
            'DOWNLOAD_DELAY': 2,
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'LOG_ENABLED': False
        }
        HTTPSpider.start_urls = [self._url]
        HTTPSpider.callback= self.received
        process.crawl(HTTPSpider)
        process.start()

    def request(self, url: str, meta: dict = None, callback = None):
        yield HTTPSpider.request(url, meta, callback)

    @abstractmethod
    def received(self, request_url: str, response_status: int, response_headers: dict, response_body: str, client):
        pass
    
class GitScraper(Scraper):
    def __init__(self, name: str, config: Config):
        super().__init__(name, config)

    def scrape(self, url: str = None):
        super().scrape(url)

        self.parse(self._config[self._name]['index_url'])

    @abstractmethod
    def parse(self, repo_url: str):
        pass