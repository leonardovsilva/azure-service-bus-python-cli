import json
import os
from json import JSONEncoder

from azure.servicebus import ServiceBusClient
from termcolor import colored
from config import config_export
from custom_log import CustomLog

CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]


class QueueProcess:
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

    def spying_message_queue(self):
        max_message_count = 2 if config_export['DEFAULT']['MaxMessageCount'] is None else int(
            config_export['DEFAULT']['MaxMessageCount'])
        save_messages_to_file = False if config_export['DEFAULT']['SaveMessagesToFile'] is None else bool(
            config_export['DEFAULT']['SaveMessagesToFile'])

        if save_messages_to_file:
            CustomLog.log_info("Starting receipt")

        print(colored('Starting receipt', 'green'))

        with self.servicebus_client:
            receiver = self.servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=max_message_count)

                if save_messages_to_file:
                    CustomLog.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                print(colored('Number of messages:', 'magenta'), colored(len(received_msgs), 'magenta'))

                for msg in received_msgs:
                    json_str = json.dumps(msg, cls=ServiceBusCustomEncoder)
                    print(json_str)

        print(colored('Receive is done', 'green'))

        if save_messages_to_file:
            CustomLog.log_info("Receive is done")


class ServiceBusCustomEncoder(JSONEncoder):
    def default(self, obj):
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_')]:
            data = getattr(obj, field)
            try:
                fields[field] = str(data)
            except TypeError:
                fields[field] = None

        return fields
