import logging
import logging.config
import os
import tomllib
from abc import ABC

with open(os.environ.get('CONFIG_PATH', '/app/conf/settings.toml'), 'rb') as f:
    config = tomllib.load(f)

    os.makedirs(os.path.dirname(config['log']['filepath']), exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
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
