import configparser
import os
import custom_log


class Config:

    config_export = configparser.SafeConfigParser()

    def init(self, verbose=False):
        for loc in os.curdir, os.path.expanduser("~"), "/etc/servicebus", os.environ.get("SERVICEBUS_CONF"):
            try:
                Config.config_export.read(os.path.join(loc, "servicebus.conf"))
            except Exception:
                pass

        custom_log_obj = custom_log.CustomLog(self, verbose)
        if verbose:
            custom_log_obj.log_info("Load configs")
            custom_log_obj.log_info("%s %s" % ('MaxMessageCount:',  Config.config_export['DEFAULT']['MaxMessageCount']))
            custom_log_obj.log_info("%s %s" % ('MaxMessageCount:', Config.config_export['DEFAULT']['SaveMessagesToFile']))

