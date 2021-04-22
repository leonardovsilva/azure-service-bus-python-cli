import configparser
import os

config_export = configparser.SafeConfigParser()


def init():
    for loc in os.curdir, os.path.expanduser("~"), "/etc/servicebus", os.environ.get("SERVICEBUS_CONF"):
        try:
            config_export.read(os.path.join(loc, "servicebus.conf"))
        except Exception:
            pass
    print("Load configs")
    print("%s %s" %('MaxMessageCount:', config_export['DEFAULT']['MaxMessageCount'],))

