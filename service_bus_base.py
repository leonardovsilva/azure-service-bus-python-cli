import os
import azure.servicebus


class ServiceBusBase:
    CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']

    service_bus_client = azure.servicebus.ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
