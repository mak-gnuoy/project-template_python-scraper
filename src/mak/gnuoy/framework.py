from abc import ABC, abstractmethod
import json
import logging
import logging.config
import tomllib
from urllib.parse import urlparse

with open("/app/conf/settings.toml", "rb") as f:
    config = tomllib.load(f)

with open(config["log"]["config"]["filepath"], "rb") as f:
    logging_config = json.load(f)
    logging.config.dictConfig(logging_config)


class Config:
    @classmethod
    def load(cls, path: str) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)


class Base(ABC):
    def __init__(self, config: dict | None = None):
        self._logger = logging.getLogger()
        self._config = config


class Store(Base):
    def __init__(self, url: str):
        super().__init__()

        self._url = url

    @classmethod
    def get_instance(cls, url: str):
        parsed_url = urlparse(url)
        if parsed_url.scheme.lower() == "file" or parsed_url.scheme.lower() == "":
            from mak.gnuoy.store import FileStore

            return FileStore.get_instance(url)
        else:
            raise Exception("Unsupported store type")

    @abstractmethod
    def set(self, **key_values):
        pass

    @abstractmethod
    def get(self, *keys):
        pass

class Scraper(Base):
    def __init__(self, name: str, config: Config):
        super().__init__(config)

        self._name = name
        # self._config = config

        # self._logger = logging.getLogger(__name__)
        # self._logger.propagate = False
        # self._logger.setLevel(self._config['log']['level'])

        # file_hanlder = logging.handlers.RotatingFileHandler(
        #             self._config['log']['filepath'],
        #             maxBytes = 10485760,
        #             backupCount =100)
        # file_hanlder.setFormatter(logging.Formatter(self._config['log']['format']))
        # self._logger.addHandler(file_hanlder)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(logging.Formatter(self._config['log']['format']))
        # self._logger.addHandler(stream_handler)

    def scrape(self, url: str | None = None):
        if url is None:
            self._url = self._config[self._name]['index_url']
        else:
            self._url = url
