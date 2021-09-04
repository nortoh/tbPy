from enum_types.event_type import EventType
from bot_events.event import Event
from chat.user import User
from chat.channel import Channel

class JoinEvent(Event):

    def __init__(self, user: User, channel: Channel):
        super().__init__(EventType.JOIN)
        self.__user__ = user
        self.__channel__ = channel

    def user(self):
        return self.__user__
    
    def channel(self):
        return self.__channel__

    