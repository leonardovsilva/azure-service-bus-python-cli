import json
import os
import config
import custom_log
import service_bus_base
import service_bus_custom_encoder

QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]


class QueueProcess(service_bus_base.ServiceBusBase):

    @staticmethod
    def spying_message_queue():
        config_obj = config.Config()
        custom_log_obj = custom_log.CustomLog(config_obj)
        max_message_count = 2 if config_obj.config_export['DEFAULT']['MaxMessageCount'] is None else int(
            config_obj.config_export['DEFAULT']['MaxMessageCount'])

        with QueueProcess.service_bus_client:
            receiver = QueueProcess.service_bus_client.get_queue_receiver(queue_name=QUEUE_NAME)
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=max_message_count)

                custom_log_obj.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                for msg in received_msgs:
                    json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
                    print(json_str)
