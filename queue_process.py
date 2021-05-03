import json

from azure.core.exceptions import AzureError
from azure.servicebus import ServiceBusReceiver, ServiceBusSender

import service_bus_base
from message_parser import ServiceBusMessageParser


class QueueProcess(service_bus_base.ServiceBusBase):

    def __init__(self, ctx):
        service_bus_base.ServiceBusBase.__init__(self, ctx)

    def spying_message_queue(self):
        with self.service_bus_client:

            if self.ctx.obj['GET_QUEUE_PROPERTIES']:
                QueueProcess.get_queue_properties(self)

            receiver = QueueProcess.get_receiver(self)

            with receiver:
                sequence_number = 0
                for x in range(self.ctx.obj['PAGES']):
                    if sequence_number == 0:
                        received_msgs = receiver.peek_messages(max_message_count=self.ctx.obj['MAX_MESSAGE_COUNT'])
                    else:
                        received_msgs = receiver.peek_messages(max_message_count=self.ctx.obj['MAX_MESSAGE_COUNT'],
                                                               sequence_number=sequence_number+1)

                    self.custom_log_obj.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                    for msg in received_msgs:
                        if self.ctx.obj['PRETTY']:
                            QueueProcess.log_message_pretty(self, msg)
                        else:
                            QueueProcess.log_message(self, msg)
                        sequence_number = msg.sequence_number

    def get_queue_properties(self):
        self.custom_log_obj.log_info("-- Get Queue Runtime Properties")
        try:
            get_queue_runtime_properties = self.servicebus_mgmt_client.get_queue_runtime_properties(self.ctx.obj['QUEUE_NAME'])
            get_queue_properties = self.servicebus_mgmt_client.get_queue(self.ctx.obj['QUEUE_NAME'])

            self.custom_log_obj.log_info("-- Authorization Rules")
            for x in get_queue_properties.authorization_rules:
                self.custom_log_obj.log_info("%s %s" % ('Rights:', x.rights,))
                self.custom_log_obj.log_info("%s %s" % ('Primary key:', x.primary_key,))
                self.custom_log_obj.log_info("%s %s" % ('Secondary key:', x.secondary_key,))
                self.custom_log_obj.log_info("%s %s" % ('Key name:', x.key_name,))
                self.custom_log_obj.log_info("%s %s" % ('Claim type:', x.claim_type,))
                self.custom_log_obj.log_info("%s %s" % ('Claim value:', x.claim_value,))
                self.custom_log_obj.log_info("%s %s" % ('Modified time utc:', x.modified_at_utc,))
                self.custom_log_obj.log_info("%s %s" % ('Created time utc:', x.created_at_utc,))
            self.custom_log_obj.log_info("-- Queue Information")
            self.custom_log_obj.log_info("%s %s" % ('Status:', get_queue_properties.status,))
            self.custom_log_obj.log_info("%s %s" % ('Queue name:', get_queue_runtime_properties.name,))
            self.custom_log_obj.log_info("%s %s" % ('Size in bytes: ', get_queue_runtime_properties.size_in_bytes,))
            self.custom_log_obj.log_info("%s %s" % ('Created at utc: ', get_queue_runtime_properties.created_at_utc,))
            self.custom_log_obj.log_info("%s %s" % ('Updated at utc: ', get_queue_runtime_properties.updated_at_utc,))
            self.custom_log_obj.log_info("%s %s" % ('Accessed at utc: ', get_queue_runtime_properties.accessed_at_utc,))
            self.custom_log_obj.log_info("%s %s" % ('Active message count:', get_queue_runtime_properties.active_message_count,))
            self.custom_log_obj.log_info("%s %s" % ('Dead letter message count:', get_queue_runtime_properties.dead_letter_message_count,))
            self.custom_log_obj.log_info("%s %s" % ('Scheduled message count:', get_queue_runtime_properties.scheduled_message_count,))
            self.custom_log_obj.log_info("%s %s" % ('Transfer message count:', get_queue_runtime_properties.transfer_message_count,))
            self.custom_log_obj.log_info("%s %s" % ('Transfer DLQ message count:', get_queue_runtime_properties.transfer_dead_letter_message_count,))
            self.custom_log_obj.log_info("%s %s" % ('Message count:', get_queue_runtime_properties.total_message_count,))

        except AzureError:
            self.custom_log_obj.log_info("Not authorized or invalid request to obtaining queue runtime properties")

    def get_receiver(self) -> ServiceBusReceiver:
        if self.ctx.obj['DEAD_LETTER']:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'],
                                                                  sub_queue=self.DEAD_LETTER)
        else:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'])

        return receiver

    def get_receiver_mode(self, receive_mode: str) -> ServiceBusReceiver:
        if self.ctx.obj['DEAD_LETTER']:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'],
                                                                  sub_queue=self.DEAD_LETTER, receive_mode=receive_mode)
        else:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'],
                                                                  receive_mode=receive_mode)

        return receiver

    def get_sender(self) -> ServiceBusSender:
        return self.service_bus_client.get_queue_sender(queue_name=self.ctx.obj['QUEUE_NAME'])

    def purge(self):
        self.custom_log_obj.log_info("Purge queue started. Wait for completion")

        QueueProcess.__purge_recursive(self, self.ctx.obj['MAX_MESSAGE_COUNT'])

        self.custom_log_obj.log_info("Purge queue completed")

    def __purge_recursive(self,  max_message_count):
        if self.ctx.obj['TO_DEAD_LETTER']:
            receiver = QueueProcess.get_receiver(self)
        else:
            receiver = QueueProcess.get_receiver_mode(self, self.ServiceBusReceiveMode.RECEIVE_AND_DELETE)

        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=max_message_count, max_wait_time=5)
            len_received_msgs = len(received_msgs)
            for msg in received_msgs:
                if self.ctx.obj['LOG_PATH'] is not None:
                    QueueProcess.log_message(self, msg)
                if self.ctx.obj['TO_DEAD_LETTER'] and not self.ctx.obj['DEAD_LETTER']:
                    receiver.dead_letter_message(msg)

        self.custom_log_obj.log_info("%s %s" % ('Length received_msgs: ', len_received_msgs,))

        if len_received_msgs is not None and len_received_msgs > 0:
            QueueProcess.__purge_recursive(self, max_message_count)

    def message(self, input_file):
        json_messages = json.load(input_file)

        with self.service_bus_client:
            sender = self.get_sender()
            with sender:
                batch_message = sender.create_message_batch()
                for message in json_messages:
                    message_parser = ServiceBusMessageParser(**message)
                    message_obj = message_parser.get_service_bus_message()
                    try:
                        batch_message.add_message(message_obj)
                    except ValueError:
                        # ServiceBusMessageBatch object reaches max_size.
                        # New ServiceBusMessageBatch object can be created here to send more data.
                        pass
                    sender.send_messages(batch_message)



