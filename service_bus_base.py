import os

from azure.servicebus import ServiceBusClient, management,  ServiceBusSubQueue


class ServiceBusBase:
    CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
    service_bus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    servicebus_mgmt_client = management.ServiceBusAdministrationClient.from_connection_string(conn_str=CONNECTION_STR)
    DEAD_LETTER = ServiceBusSubQueue.DEAD_LETTER

    @staticmethod
    def dump(obj):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))