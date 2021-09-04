from enum_types.event_type import EventType
from bot_events.event import Event
from chat.user import User
from chat.channel import Channel

class PartEvent(Event):

    def __init__(self, user: User, channel: Channel):
        super().__init__(EventType.PART)
        self.__user = user
        self.__channel = channel

    def user(self):
        return self.__user
    
    def channel(self):
        return self.__channel

    