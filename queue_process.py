import os
from azure.servicebus import ServiceBusClient
from termcolor import colored

CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]


class QueueProcess:
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

    def spying_message_queue(self):
        print(colored('Starting receipt', 'green'))

        with self.servicebus_client:
            receiver = self.servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=2)

                print(colored('Number of messages:', 'magenta'), colored(len(received_msgs), 'magenta'))

                for msg in received_msgs:
                    print(str(msg))

        print(colored('Receive is done', 'green'))
