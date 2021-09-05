from ..types.event_type import EventType
from ..events.event import Event
from ..chat.user import User
from ..chat.channel import Channel
from ..chat.message import Message

import string

class MessageEvent(Event):

    def __init__(self, user: User, channel: Channel, message: Message):
        super().__init__(EventType.MESSAGE)
        self.__user__ = user
        self.__channel__ = channel
        self.__message__ = message

    def user(self):
        return self.__user__
    
    def channel(self):
        return self.__channel__

    def message(self):
        return self.__message__