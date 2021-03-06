import asyncio
import websockets
import logging

from ...chat.channel import Channel
from .twitch_conn import TwitchConnection

class TwitchWS(TwitchConnection):

    def __init__(self, bot):
        self.logger = logging.getLogger('main')
        self.bot = bot

    async def connect(self):
        self.websocket = await websockets.connect("ws://irc-ws.chat.twitch.tv:80")
    
    async def close(self):
        self.websocket.close()
    
    async def send(self, message):
        await self.websocket.send(str.encode(message + "\r\n"))

    async def receive(self):
        response = await self.websocket.recv()
        return response
        
    async def join_channel(self, channel):
        if isinstance(channel, Channel):
            await self.send_raw_message("JOIN " + channel.name())
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
            self.send_raw_message_noasync("JOIN " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_raw_message_noasync("JOIN " + channel)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)

    async def part_channel(self, channel):
        if isinstance(channel, Channel):
            await self.send_raw_message("PART " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                await self.send_raw_message("PART " + channel)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)

    def part_channel_noasync(self, channel):
        if isinstance(channel, Channel):
            self.send_raw_message_noasync("PART " + channel.name())
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_raw_message_noasync("PART " + channel)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)

    async def send_message(self, channel, message):
        if isinstance(channel, Channel):
            await self.send_raw_message("PRIVMSG " + channel.name() + " :" + message)
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                await self.send_raw_message("PRIVMSG " + channel + " :" + message)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)
    
    def send_message_noasync(self, channel, message):
        if isinstance(channel, Channel):
            self.send_raw_message_noasync("PRIVMSG " + channel.name() + " :" + message)
        elif isinstance(channel, str):
            try:
                if not str.startswith(channel, '#'):
                    raise Exception("Invalid channel format. Please include a # in front of ", channel)
                    return
                self.send_raw_message_noasync("PRIVMSG " + channel + " :" + message)
            except Exception as e:
                message, channel_name = e.args
                self.logger.error(message + channel_name)