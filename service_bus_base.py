import os
import custom_log
from azure.servicebus import ServiceBusClient, management, ServiceBusSubQueue


class ServiceBusBase:

    def __init__(self, ctx):
        self.ctx = ctx
        self.CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
        self.SERVICE_BUS_QUEUE_NAME = None
        self.SERVICE_BUS_TOPIC_NAME = None
        self.SERVICE_BUS_SUBSCRIPTION_NAME = None

        self.custom_log_obj = custom_log.CustomLog(ctx.obj['VERBOSE'],  ctx.obj['LOG_PATH'])
        self.service_bus_client = ServiceBusClient.from_connection_string(conn_str=self.CONNECTION_STR)
        self.servicebus_mgmt_client = management.ServiceBusAdministrationClient.from_connection_string(conn_str=self.CONNECTION_STR)
        self.DEAD_LETTER = ServiceBusSubQueue.DEAD_LETTER

        ServiceBusBase.init_variables(self)

    def init_variables(self):

        try:
            self.SERVICE_BUS_QUEUE_NAME = os.environ['SERVICE_BUS_QUEUE_NAME']
            self.ctx.obj['QUEUE_NAME'] = self.SERVICE_BUS_QUEUE_NAME
        except KeyError:
            self.custom_log_obj.log_info("Environment variable 'SERVICE_BUS_QUEUE_NAME' not defined")

        try:
            self.SERVICE_BUS_TOPIC_NAME = os.environ['SERVICE_BUS_TOPIC_NAME']
            self.ctx.obj['TOPIC_NAME'] = self.SERVICE_BUS_TOPIC_NAME
        except KeyError:
            self.custom_log_obj.log_info("Environment variable 'SERVICE_BUS_TOPIC_NAME' not defined")

        try:
            self.SERVICE_BUS_SUBSCRIPTION_NAME = os.environ['SERVICE_BUS_SUBSCRIPTION_NAME']
            self.ctx.obj['SUBSCRIPTION_NAME'] = self.SERVICE_BUS_SUBSCRIPTION_NAME
        except KeyError:
            self.custom_log_obj.log_info("Environment variable 'SERVICE_BUS_SUBSCRIPTION_NAME' not defined")

    @staticmethod
    def dump(obj):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))