from ..enum_types import EventType
from ..bot_events import Event
from ..chat import User
from ..chat import Channel
from ..chat import Message

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