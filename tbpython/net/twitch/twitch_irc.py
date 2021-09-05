import socket
import logging

from ....chat import Channel
from . import TwitchConnection

class TwitchIRC(TwitchConnection):

    socket = None

    def __init__(self, bot):
        self.logger = logging.getLogger('main')
        self.bot = bot
        
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    async def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("irc.twitch.tv", 6667))

    async def close(self):
        self.socket.close()

    async def receive(self) -> str:
        reader = getattr(self.socket, 'read', self.socket.recv)
        return reader(2 ** 14)

    async def send(self, message):
        if self.bot.reconnect_flag:
            return
        self.socket.sendall(str.encode(message + "\r\n"))
    
    def send_sync(self, message):
        if self.bot.reconnect_flag:
            return
        self.socket.sendall(str.encode(message + "\r\n"))

    async def join_channel(self, channel):
        if isinstance(channel, Channel):
            await self.send("JOIN " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                await self.send_raw_message("JOIN " + channel)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)

    def join_channel_noasync(self, channel):
        if isinstance(channel, Channel):
            self.send_sync("JOIN " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_sync("JOIN " + channel)
            except Exception as e:
                self.logger.error(e)

    async def part_channel(self, channel):
        if isinstance(channel, Channel):
            await self.send("PART " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                await self.send("PART " + channel)
            except Exception as e:
                self.logger.error(e)

    def part_channel_noasync(self, channel):
        if isinstance(channel, Channel):
            self.send_sync("PART " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_sync("PART " + channel)
            except Exception as e:
                self.logger.error(e)

    async def send_message(self, channel, message):
        if isinstance(channel, Channel):
            await self.send("PRIVMSG " + channel.name() + " :" + message)
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                await self.send("PRIVMSG " + channel + " :" + message)
            except Exception as e:
                self.logger.error(e)
    
    def send_message_noasync(self, channel, message):
        if isinstance(channel, Channel):
            self.send_sync("PRIVMSG " + channel.name() + " :" + message)
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_sync("PRIVMSG " + channel + " :" + message)
            except Exception as e:
                self.logger.error(e)