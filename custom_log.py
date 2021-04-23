import logging
import os
import time

loggers = {}
config_obj = None
is_verbose = False


class CustomLog:

    def __init__(self,  config, verbose):
        global config_obj, is_verbose
        is_verbose = verbose
        config_obj = config

    @staticmethod
    def get_logger(logger_name):
        global loggers

        if loggers.get(logger_name):
            return loggers.get(logger_name)
        else:
            if is_verbose:
                root_logger = logging.getLogger()
            else:
                root_logger = logging.getLogger(logger_name)

            try:
                log_path = config_obj.config_export['DEFAULT']['LogPath']
            except Exception:
                log_path = os.path.dirname(os.path.abspath(__file__))

            save_messages_to_file = False if config_obj.config_export['DEFAULT']['SaveMessagesToFile'] is None else bool(
                config_obj.config_export['DEFAULT']['SaveMessagesToFile'])

            log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

            root_logger.setLevel(logging.INFO)

            if save_messages_to_file:
                file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, time.strftime("%Y%m%d")))
                file_handler.setFormatter(log_formatter)
                root_logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            root_logger.addHandler(console_handler)
            loggers[logger_name] = root_logger

            return root_logger

    @staticmethod
    def log_info(message):
        root_logger = CustomLog.get_logger("azure-log")
        root_logger.info(message)

