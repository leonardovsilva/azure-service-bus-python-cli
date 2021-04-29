import configparser
import os


class Config:

    config_export = configparser.SafeConfigParser()

    @staticmethod
    def init():
        for loc in os.curdir, os.path.expanduser("~"), "/etc/servicebus", os.environ.get("SERVICEBUS_CONF"):
            try:
                Config.config_export.read(os.path.join(loc, "servicebus.conf"))
            except Exception:
                pass

