import logging
import logging.config
import os
import tomllib
from abc import ABC, abstractmethod
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
