import json

from azure.core.exceptions import AzureError
import service_bus_base
import service_bus_custom_encoder


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
                        print(sequence_number)

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
            self.custom_log_obj.log_info("Not authorized or invalid request to obtaining  queue runtime properties")

    def get_receiver(self):
        if self.ctx.obj['DEAD_LETTER']:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'], sub_queue=self.DEAD_LETTER)
        else:
            receiver = self.service_bus_client.get_queue_receiver(queue_name=self.ctx.obj['QUEUE_NAME'])

        return receiver

    def log_message_pretty(self, msg):
        self.custom_log_obj.log_info("%s %s" % ('Message encoded size: ', msg.message.get_message_encoded_size(),))
        json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
        json_obj = json.loads(json_str)
        json_obj["application_properties"] = json.loads(json_obj["application_properties"].replace("b'", "'").replace("'", '"').replace("None", '""'))
        try:
            json_obj["message"] = json.loads(json_obj["message"])
        except Exception:
            pass
        json_str = json.dumps(json_obj, indent=4)
        self.custom_log_obj.log_info(json_str)

    def log_message(self, msg):
        self.custom_log_obj.log_info("%s %s" % ('Message encoded size: ', msg.message.get_message_encoded_size(),))
        json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
        self.custom_log_obj.log_info(json_str.replace("\\", ""))

    def purge_queue(self):
        receiver = QueueProcess.get_receiver(self)

        self.custom_log_obj.log_info("Purge queue started. Wait for completion")
        with receiver:
            QueueProcess.__purge_queue_recursive(self, self.ctx.obj['MAX_MESSAGE_COUNT'], receiver)

        self.custom_log_obj.log_info("Purge queue completed")

    def __purge_queue_recursive(self,  max_message_count, receiver):

        received_msgs = receiver.receive_messages(max_message_count=max_message_count, max_wait_time=5)
        len_received_msgs = len(received_msgs)
        for msg in received_msgs:
            if self.ctx.obj['LOG_PATH'] is not None:
                QueueProcess.log_message(self, msg)
            receiver.complete_message(msg)

        if len_received_msgs is not None and len_received_msgs == max_message_count:
            QueueProcess.__purge_queue_recursive(self, max_message_count, receiver)

