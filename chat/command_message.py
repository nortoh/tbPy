import string

from chat.channel import Channel
from chat.user import User

class CommandMessage(object):

    def __init__(self, command: string, parameters: string, channel: Channel, sender: User, timestamp: float):
        self.__command__ = command
        self.__channel__ = channel
        self.__sender__ = sender
        self.__timestamp__ = timestamp
        self.__parameters__ = parameters

    def command(self):
        return self.__command__
    
    def channel(self) -> Channel:
        return self.__channel__
    
    def sender(self) -> User:
        return self.__sender__
    
    def timestamp(self):
        return self.__timestamp__

    def parameters(self):
        return self.__parameters__