from abc import ABC, abstractmethod
import logging
import logging.config
import os
import tomllib
from urllib.parse import urlparse

with open(os.environ.get('CONFIG_PATH', '/app/conf/default.toml'), 'rb') as f:
    config = tomllib.load(f)

    os.makedirs(os.path.dirname(config['log']['filepath']), exist_ok=True)
    logging.basicConfig(
        level=config['log']['level'],
        format=config['log']['format'],
        handlers=[
            logging.handlers.RotatingFileHandler(
                config['log']['filepath'],
                maxBytes = 10485760,
                backupCount =100),
            logging.StreamHandler()
        ]
    )

class Base(ABC):
    def __init__(self):
        self.logger = logging.getLogger()

class Config(Base):
    @classmethod
    def load(cls, path: str) -> dict:
        with open(path, 'rb') as f:
            config = tomllib.load(f)
        return config

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
        super().__init__()

        self._name = name
        self._config = config

        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(self._config['log']['level'])

        file_hanlder = logging.handlers.RotatingFileHandler(
                    self._config['log']['filepath'],
                    maxBytes = 10485760,
                    backupCount =100)
        file_hanlder.setFormatter(logging.Formatter(self._config['log']['format']))
        self.logger.addHandler(file_hanlder)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self._config['log']['format']))
        self.logger.addHandler(stream_handler)

    def scrape(self, url: str = None):
        if url is None:
            self._url = self._config[self._name]['index_url']
        else:
            self._url = url
