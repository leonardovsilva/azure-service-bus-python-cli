import json
from azure.core.exceptions import AzureError
import service_bus_base
import service_bus_custom_encoder


class QueueProcess(service_bus_base.ServiceBusBase):

    def __init__(self, ctx):
        service_bus_base.ServiceBusBase.__init__(self, ctx)

    def spying_message_queue(self):

        max_message_count = 5 if self.ctx.obj['MAX_MESSAGE_COUNT'] is None else int(self.ctx.obj['MAX_MESSAGE_COUNT'])

        with self.service_bus_client:

            if self.ctx.obj['GET_QUEUE_PROPERTIES']:
                QueueProcess.get_queue_properties()

            if self.ctx.obj['DEAD_LETTER']:
                receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'],
                                                                              sub_queue=self.DEAD_LETTER)
            else:
                receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'])
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=max_message_count)

                self.custom_log_obj.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                for msg in received_msgs:
                    json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
                    json_str = json_str.replace('\\"', '"')
                    self.custom_log_obj.log_info(json_str)

    def get_queue_properties(self):
        self.custom_log_obj.log_info("-- Get Queue Runtime Properties")
        try:
            get_queue_runtime_properties = self.servicebus_mgmt_client.get_queue_runtime_properties(self.ctx.obj['QUEUE_NAME'])
            self.custom_log_obj.log_info("%s %s" % ('Queue Name:', get_queue_runtime_properties.name,))
            self.custom_log_obj.log_info("%s %s" % ('Updated at: ', get_queue_runtime_properties.updated_at_utc,))
            self.custom_log_obj.log_info("%s %s" % ('Size in Bytes: ', get_queue_runtime_properties.size_in_bytes,))
            self.custom_log_obj.log_info("%s %s" % ('Message Count:', get_queue_runtime_properties.total_message_count,))
        except AzureError:
            self.custom_log_obj.log_info("Not authorized or invalid request to obtaining  queue runtime properties")
