import logging

from mak.gnuoy.framework import Base

class World(Base):
    def hello(self):
        self.logger.info("hello")

if __name__ == '__main__':
    logging.getLogger().info("hello wolrd")
    World().hello()
    