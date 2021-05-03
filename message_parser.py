from datetime import datetime, timedelta
from typing import Optional, Any

from azure.servicebus import ServiceBusMessage


class ServiceBusMessageParser:
    """Service Bus message properties."""

    def __init__(
            self,
            application_properties,
            session_id,
            message_id,
            scheduled_enqueue_time_utc,
            time_to_live,
            content_type,
            correlation_id,
            subject,
            partition_key,
            to,
            reply_to,
            reply_to_session_id,
            message
    ):
        self._application_properties = application_properties  # type: Optional[dict]
        self._session_id = session_id  # type: Optional[str]
        self._message_id = message_id  # type: Optional[str]
        self._scheduled_enqueue_time_utc = scheduled_enqueue_time_utc  # type: Optional[datetime]
        self._time_to_live = time_to_live  # type: Optional[datetime]
        self._content_type = content_type  # type: Optional[str]
        self._correlation_id = correlation_id  # type: Optional[str]
        self._subject = subject  # type: Optional[str]
        self._partition_key = partition_key  # type: Optional[str]
        self._to = to  # type: Optional[str]
        self._reply_to = reply_to  # type: Optional[str]
        self._reply_to_session_id = reply_to_session_id  # type: Optional[str]
        self._message = message  # type: Any

    @property
    def application_properties(self):
        return self._application_properties

    @property
    def session_id(self):
        return self._session_id

    @property
    def message_id(self):
        return self._message_id

    @property
    def scheduled_enqueue_time_utc(self):
        if self._scheduled_enqueue_time_utc is not None:
            self._scheduled_enqueue_time_utc = datetime.strptime(self._scheduled_enqueue_time_utc, '%Y-%m-%dT%H:%M:%SZ')
        return self._scheduled_enqueue_time_utc

    @property
    def time_to_live(self):
        if self._time_to_live is not None:
            datetime_1 = datetime.now()
            datetime_2 = datetime.strptime(self._time_to_live, '%Y-%m-%dT%H:%M:%SZ')
            a_timedelta = datetime_2 - datetime_1
            self._time_to_live = a_timedelta

        return self._time_to_live

    @property
    def content_type(self):
        return self._content_type

    @property
    def correlation_id(self):
        return self._correlation_id

    @property
    def subject(self):
        return self._subject

    @property
    def partition_key(self):
        return self._partition_key

    @property
    def to(self):
        return self._to

    @property
    def reply_to(self):
        return self._reply_to

    @property
    def reply_to_session_id(self):
        return self._reply_to_session_id

    @property
    def message(self):
        return self._message

    @staticmethod
    def get_instance(json_dict):
        return ServiceBusMessageParser(**json_dict)

    def get_service_bus_message(self):
        # type: () -> ServiceBusMessage

        parameters = {"application_properties": self.application_properties, "session_id": self.session_id,
                      "message_id": self.message_id, "scheduled_enqueue_time_utc": self.scheduled_enqueue_time_utc,
                      "time_to_live": self.time_to_live, "content_type": self.content_type,
                      "correlation_id": self.correlation_id, "subject": self.subject,
                      "partition_key": self.partition_key, "to": self.to, "reply_to": self.reply_to,
                      "reply_to_session_id": self.reply_to_session_id}

        return ServiceBusMessage(self.message, **{k: v for k, v in parameters.items() if v is not None and v != ''})
