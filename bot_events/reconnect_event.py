from enum_types.event_type import EventType
from bot_events.event import Event

class ReconnectEvent(Event):

    def __init__(self, sleep_time):
        super().__init__(EventType.RECONNECT)
        self.__sleep_time__ = sleep_time

    def sleep_time(self):
        return self.__sleep_time__