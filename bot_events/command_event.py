from enum_types.event_type import EventType
from bot_events.event import Event
from chat.user import User
from chat.channel import Channel
from chat.message import Message
from chat.command_message import CommandMessage
from net.twitch.twitch_irc import TwitchIRC
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