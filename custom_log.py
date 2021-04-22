import logging
import os
import time


class CustomLog:
    root_logger = logging.getLogger()

    def __init__(self, config_obj):
        try:
            log_path = config_obj.config_export['DEFAULT']['LogPath']
        except Exception:
            log_path = os.path.dirname(os.path.abspath(__file__))

        save_messages_to_file = False if config_obj.config_export['DEFAULT']['SaveMessagesToFile'] is None else bool(
            config_obj.config_export['DEFAULT']['SaveMessagesToFile'])

        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        CustomLog.root_logger.setLevel(logging.INFO)

        if save_messages_to_file:
            file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, time.strftime("%Y%m%d")))
            file_handler.setFormatter(log_formatter)
            CustomLog.root_logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            CustomLog.root_logger.addHandler(console_handler)

    def log_info(self, message):
        CustomLog.root_logger.info(message)
