from azure.servicebus import ServiceBusReceiver

import service_bus_base


class TopicProcess(service_bus_base.ServiceBusBase):

    def __init__(self, ctx):
        service_bus_base.ServiceBusBase.__init__(self, ctx)

    def spying_message(self):
        with self.service_bus_client:

            receiver = TopicProcess.get_receiver(self)

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
                            TopicProcess.log_message_pretty(self, msg)
                        else:
                            TopicProcess.log_message(self, msg)
                        sequence_number = msg.sequence_number

    def purge(self):
        self.custom_log_obj.log_info("Purge subscription started. Wait for completion")

        TopicProcess.__purge_recursive(self, self.ctx.obj['MAX_MESSAGE_COUNT'])

        self.custom_log_obj.log_info("Purge subscription completed")

    def __purge_recursive(self, max_message_count):
        if self.ctx.obj['TO_DEAD_LETTER']:
            receiver = TopicProcess.get_receiver(self)
        else:
            receiver = TopicProcess.get_receiver_mode(self, self.ServiceBusReceiveMode.RECEIVE_AND_DELETE)

        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=max_message_count, max_wait_time=5)
            len_received_msgs = len(received_msgs)
            for msg in received_msgs:
                if self.ctx.obj['LOG_PATH'] is not None:
                    TopicProcess.log_message(self, msg)
                if self.ctx.obj['TO_DEAD_LETTER'] and not self.ctx.obj['DEAD_LETTER']:
                    receiver.dead_letter_message(msg)

        self.custom_log_obj.log_info("%s %s" % ('Length received_msgs: ', len_received_msgs,))
        self.custom_log_obj.log_info("%s %s" % ('Max message count: ', max_message_count,))

        if len_received_msgs is not None and len_received_msgs > 0:
            TopicProcess.__purge_recursive(self, max_message_count)

    def get_receiver(self) -> ServiceBusReceiver:
        if self.ctx.obj['DEAD_LETTER']:
            receiver = self.service_bus_client\
                .get_subscription_receiver(topic_name=self.ctx.obj['TOPIC_NAME'],
                                           subscription_name=self.ctx.obj['SUBSCRIPTION_NAME'],
                                           sub_queue=self.DEAD_LETTER)
        else:
            receiver = self.service_bus_client\
                .get_subscription_receiver(topic_name=self.ctx.obj['TOPIC_NAME'],
                                           subscription_name=self.ctx.obj['SUBSCRIPTION_NAME'],)

        return receiver

    def get_receiver_mode(self, receive_mode: str) -> ServiceBusReceiver:
        if self.ctx.obj['DEAD_LETTER']:
            receiver = self.service_bus_client\
                .get_subscription_receiver(topic_name=self.ctx.obj['TOPIC_NAME'],
                                           subscription_name=self.ctx.obj['SUBSCRIPTION_NAME'],
                                           sub_queue=self.DEAD_LETTER, receive_mode=receive_mode)
        else:
            receiver = self.service_bus_client\
                .get_subscription_receiver(topic_name=self.ctx.obj['TOPIC_NAME'],
                                           subscription_name=self.ctx.obj['SUBSCRIPTION_NAME'],
                                           receive_mode=receive_mode)

        return receiver
