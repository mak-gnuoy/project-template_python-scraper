import logging
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

from mak.gnuoy.framework import Config
from mak.gnuoy.scraper import ScrapyScraper


class ToScapeScraper(ScrapyScraper):

    def received(self, response):
        self._logger.info(
            f"status={response['status']} request_url={response['request']['url']}"
        )

        if response["status"] == 200:
            try:
                bs = BeautifulSoup(response["body"], "html.parser")
                href = bs.select("nav ul li.next a")[0].get("href")
                parsed_url = urlparse(response["url"])
                next_url = urlunparse(parsed_url._replace(path=href))

                return self.client.request(
                    url=next_url, headers=self._config["headers"]
                )
            except IndexError as e:
                self._logger.info(f"all done. end of page")


if __name__ == "__main__":
    logging.getLogger().info("Scraping is started.")
    config = Config.load("conf/toscrape.toml")
    scraper = ToScapeScraper(config["toscrape"], config["settings"])
    scraper.scrape()
    logging.getLogger().info("Scraping is done.")
