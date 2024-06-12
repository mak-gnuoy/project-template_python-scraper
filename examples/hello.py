import logging

from mak.gnuoy.framework import Base

class World(Base):
    def hello(self):
        self.logger.info("hello, world")

if __name__ == '__main__':
    logging.getLogger().info("python project example")
    World().hello()