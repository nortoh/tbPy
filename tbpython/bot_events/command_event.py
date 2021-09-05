from ..enum_types import EventType
from ..bot_events import Event
from ..chat import User
from ..chat import Channel
from ..chat import Message
from ..chat import CommandMessage
from ..net.twitch import TwitchIRC
import string

class CommandEvent(Event):

    def __init__(self, user: User, channel: Channel, command_message: CommandMessage, twitch_irc: TwitchIRC):
        super().__init__(EventType.COMMAND)
        self.__user__ = user
        self.__channel__ = channel
        self.__command_message__ = command_message
        self.__twitch_irc__ = twitch_irc

    def user(self):
        return self.__user__
    
    def channel(self):
        return self.__channel__

    def command_message(self):
        return self.__command_message__
    
    def twitch_irc(self):
        return self.__twitch_irc__