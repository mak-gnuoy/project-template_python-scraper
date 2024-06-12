import logging

from mak.gnuoy.store import JsonFileStore

if __name__ == '__main__':
    logging.getLogger().info("python project example")
 
    store = JsonFileStore("/app/output/hello.json")
    store.set(**{'hello': 'hello, world from store'})
    hello_dict = store.get('hello')
    logging.getLogger().info(f"{hello_dict['hello']}")

    