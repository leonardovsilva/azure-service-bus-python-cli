import json
from azure.core.exceptions import AzureError
import custom_log
import service_bus_base
import service_bus_custom_encoder


class QueueProcess(service_bus_base.ServiceBusBase):

    @staticmethod
    def spying_message_queue(ctx):
        custom_log_obj = custom_log.CustomLog(ctx.obj['VERBOSE'], ctx.obj['LOG_PATH'])
        max_message_count = 5 if ctx.obj['MAX_MESSAGE_COUNT'] is None else int(ctx.obj['MAX_MESSAGE_COUNT'])

        print(max_message_count)
        with QueueProcess.service_bus_client:
            QueueProcess.get_queue_properties(ctx)
            receiver = QueueProcess.service_bus_client.get_queue_receiver(queue_name=ctx.obj['QUEUE_NAME'])
            with receiver:
                received_msgs = receiver.peek_messages(max_message_count=max_message_count)

                custom_log_obj.log_info("%s %s" % ('Number of messages: ', len(received_msgs),))

                for msg in received_msgs:
                    json_str = json.dumps(msg, cls=service_bus_custom_encoder.ServiceBusCustomEncoder)
                    custom_log_obj.log_info(json_str)

    @staticmethod
    def get_queue_properties(ctx):
        print("-- Get Queue Runtime Properties")
        try:
            get_queue_runtime_properties = QueueProcess.servicebus_mgmt_client.get_queue_runtime_properties(ctx.obj['QUEUE_NAME'])
            print("Queue Name:", get_queue_runtime_properties.name)
            print("Queue Runtime Properties:")
            print("Updated at:", get_queue_runtime_properties.updated_at_utc)
            print("Size in Bytes:", get_queue_runtime_properties.size_in_bytes)
            print("Message Count:", get_queue_runtime_properties.total_message_count)
            print("Please refer to QueueRuntimeProperties from complete available runtime properties.")
            print("")
        except AzureError:
            print("Not authorized or invalid request to obtaining  queue runtime properties")
