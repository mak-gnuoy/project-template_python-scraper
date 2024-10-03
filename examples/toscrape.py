import datetime
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

from mak.gnuoy.framework import Config
from mak.gnuoy.scraper import ScrapyScraper


class ToScapeScraper(ScrapyScraper):

    def received(self, response):
        self._logger.info(
            f"status={response['status']} request_url={response['request']['url']}"
        )

        if response["status"] == 200:
            try:
                timestamp = datetime.datetime.now(datetime.UTC).timestamp()

                # save received index page to the file
                index_output_path = os.path.join(
                    self._root_output_path,
                    datetime.datetime.now(datetime.UTC).strftime("%Y/%m/%d/%H"),
                )
                pattern = re.compile(r".+page/(?P<page>\d+)/")
                matched = pattern.match(str(response["url"]))
                page = matched.group("page")  # type: ignore
                os.makedirs(index_output_path, exist_ok=True)
                with open(os.path.join(index_output_path, f"{page}.html"), "w") as f:
                    f.write(str(response["body"]))

                # get a next url
                bs = BeautifulSoup(response["body"], "html.parser")
                href = bs.select("nav ul li.next a")[0].get("href")
                parsed_url = urlparse(response["url"])
                next_url = urlunparse(parsed_url._replace(path=href))
                self._progress.set(**{"next_index_url": next_url})

                # make a request
                return self.client.request(
                    url=next_url, headers=self._config["headers"]
                )
            except IndexError as e:
                self._logger.debug(f"end of page")
                self._progress.set(**{"next_index_url": None})


if __name__ == "__main__":
    config = Config.load("conf/toscrape.toml")
    scraper = ToScapeScraper(config["settings"])
    scraper.scrape(config["toscrape"])
