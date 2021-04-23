import json
import custom_log
import service_bus_base
import service_bus_custom_encoder


class TopicProcess(service_bus_base.ServiceBusBase):

    @staticmethod
    def spying_message_topic(ctx):
        custom_log_obj = custom_log.CustomLog(ctx.obj['VERBOSE'], ctx.obj['LOG_PATH'])
        max_message_count = 5 if ctx.obj['MAX_MESSAGE_COUNT'] is None else int(ctx.obj['MAX_MESSAGE_COUNT'])

        with TopicProcess.service_bus_client:
            receiver = TopicProcess.service_bus_client.get_subscription_receiver(
                topic_name=ctx.obj['TOPIC_NAME'],
                subscription_name=ctx.obj['SUBSCRIPTION_NAME']
            )
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=max_message_count)

                custom_log_obj.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                for msg in received_msgs:
                    json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
                    custom_log_obj.log_info(json_str)
