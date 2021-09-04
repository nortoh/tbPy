from bot_events.event import Event
from enum_types.event_type import EventType
from chat.channel import Channel
from chat.tag import Tag
import string

class UserStateEvent(Event):

    def __init__(self, channel: Channel, tag: Tag):
        super().__init__(EventType.USERSTATE)
        self.__channel__ = channel
        self.__tag__ = tag
    
    def channel(self):
        return self.__channel__

    def tag(self):
        return self.__tag__
