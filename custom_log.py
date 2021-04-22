import logging


class CustomLog:

    def __init__(self):
        logging.basicConfig(filename='out.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    @staticmethod
    def log_info(message):
        logging.info(message)
