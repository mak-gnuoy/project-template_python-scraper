import logging

from mak.gnuoy.framework import Config

if __name__ == '__main__':
    logging.getLogger().info("python project example")
 
    config_dict = Config.load("conf/hello.toml")
    logging.getLogger().info(f"{config_dict['hello']['message']}")

    