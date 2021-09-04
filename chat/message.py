import string

from chat.channel import Channel
from chat.user import User
from chat.tag import Tag

class Message(object):

    def __init__(self, id: string, text: string, channel: Channel, sender: User, timestamp: float, tag: Tag):
        self.__id__ = id
        self.__text__ = text
        self.__channel__ = channel
        self.__sender__ = sender
        self.__timestamp__ = timestamp
        self.__tag__ = tag

    def id(self):
        return self.__id__
    
    def text(self):
        return self.__text__
    
    def channel(self) -> Channel:
        return self.__channel__
    
    def sender(self) -> User:
        return self.__sender__
    
    def timestamp(self):
        return self.__timestamp__

    def tag(self):
        return self.__tag__