import asyncio
import time
import os
from os import path
from socket import error as SocketError
import json
import string
import sqlite3
import logging
import datetime
from datetime import date
import socket


from ..chat import Message
from ..chat import CommandMessage
from ..chat import Channel
from ..chat import User
from ..chat import Tag
from ..chat import WordHandler
from ..commands import Command

from ..misc import Log
from ..misc import RepeatingTimer
from ..misc import Config

from ..events.event_handler import EventHandler
from ..events.connected_event import ConnectedEvent
from ..events.disconnected_event import DisconnectedEvent
from ..events.startup_event import StartUpEvent
from ..events.ping_event import PingEvent
from ..events.join_event import JoinEvent
from ..events.message_event import MessageEvent
from ..events.command_event import CommandEvent
from ..events.clear_message_event import ClearMessageEvent
from ..events.part_event import PartEvent
from ..events.notice_event import NoticeEvent
from ..events.user_notice_event import UserNoticeEvent
from ..events.user_state_event import UserStateEvent
from ..events.room_state_event import RoomStateEvent
from ..events.host_target_event import HostTargetEvent
from ..events.error_event import ErrorEvent
from ..events.newday_event import NewdayEvent
from ..events.reconnect_event import ReconnectEvent


from ..types.notice_type import NoticeType
from ..types.user_notice_type import UserNoticeType
from ..types.irc_type import IRCType

from ..net.twitch.twitch_irc import TwitchIRC
from ..net.twitch.twitch_ws import TwitchWS
from jaraco.stream import buffer

class Bot:
    
    # Main bot constructor
    def __init__(self):
        self.lib_version = 1.0

        self.logger = Log('main').setup_custom_logger()
        self.twitch_disconnects = 0
        self.start_day = int(date.today().strftime('%d'))

        # Command List
        self.commands = dict()

        # Initalize Event Handler
        self.event_handler = EventHandler()

        # Initalize Word Handler
        self.word_handler = WordHandler()

        # Load configs, commands, and database(?)
        self.load_configurations()
        self.load_builtin_commands()

        # Channels the bot is in
        self.channels = []

        self.has_finished_motd = False
        self.reconnect_flag = False
        self.connected = False

        # Start timers
        self.start_timers()

    # async start bot        
    async def start_bot(self):
        self.logger.info(f'Starting bot v{self.lib_version}')
        
        # Socket stream buffer
        self.buffer = buffer.LineBuffer()

        # Fire!
        self.event_handler.on_startup(StartUpEvent())

        # Connect to Twitch
        await self.connect_to_twitch()

    # Async connect to twitch
    async def connect_to_twitch(self):
        self.logger.info(f'Connecting to Twitch [{self.config.username}]')

        # TCP socket and data stream
        self.twitch_irc = TwitchIRC(self)
        await self.twitch_irc.connect()

        self.logger.info(f'Connected to Twitch')
        
        self.running = True

        # Set the time we successfully connected
        self.start_time = datetime.datetime.now()

        # Perform handshake
        await self.handshake()

        # Join channels in configuration
        for name in self.config.channels:
            await self.twitch_irc.send(f'JOIN {name}')
        
        # Loop and handle data
        while not self.reconnect_flag and self.running:
            try:
                # Get data
                new_data = await self.twitch_irc.receive()

                # If data was empty
                if not new_data:
                    self.logger.error('No longer receiving data from socket')
                    self.event_handler.on_error(ErrorEvent(f'No longer receiving data from socket'))
                    self.reconnect_flag = True
                    break

                # Add new data to buffer
                self.buffer.feed(new_data)

                # Process new lines
                for line in self.buffer:

                    # Skip empty
                    if not line:
                        continue

                    if self.config.verbose:
                        self.logger.info(f'Data: {line.decode()}')

                    await self.process_data(line.decode())
            except KeyboardInterrupt:
                os._exit(0)
            except SocketError as e:
                self.logger.error(f'SocketError: {e.errno}')

                # Throw error
                self.event_handler.on_error(ErrorEvent(f'SocketError: {e.errno}'))
                self.reconnect_flag = True
                break
        
        # Close socket and set socket as None
        self.logger.warning('Closing socket')
        self.twitch_irc.socket.close()
        self.twitch_irc.socket = None
        self.connected = False

        # Fire!
        self.event_handler.on_disconnected(DisconnectedEvent())

    # Process IRC line
    async def process_data(self, line):
        irc_parameters = line.split(' ')

        # If we receive 001 msg code
        if await self.expect_code(irc_parameters, '001'):
            self.connected = True
            self.event_handler.on_connected(ConnectedEvent())


        # Do nothing until we've read the end of the MOTD
        if not self.has_finished_motd:

            # Wait to read the entire MOTD before accepting events,
            # this prevents irc server info from triggering regex conditions
            if await self.expect_code(irc_parameters, '376'):
                self.has_finished_motd = True
            return

        # Grab IRC type from irc data
        irc_type = await self.convert_2_type(line)

        # PING
        if irc_type == IRCType.PING:
            await self.handle_pong(irc_parameters)
        # PRIVMSG
        elif irc_type == IRCType.PRIVMSG:
            await self.handle_message(irc_parameters)
        # JOIN
        elif irc_type == IRCType.JOIN:
            await self.handle_join(line, irc_parameters)
        # PART
        elif irc_type == IRCType.PART:
            await self.handle_part(line, irc_parameters)
        # NOTICE
        elif irc_type == IRCType.NOTICE:
            await self.handle_notice(irc_parameters)
        # USERNOTICE
        elif irc_type == IRCType.USERNOTICE:
            await self.handle_user_notice(irc_parameters)
        # USERSTATE
        elif irc_type == IRCType.USERSTATE:
            await self.handle_user_state(irc_parameters)
        # ROOMSTATE
        elif irc_type == IRCType.ROOMSTATE:
            await self.handle_room_state(irc_parameters)
        # CLEARMSG
        elif irc_type == IRCType.CLEARMSG:
            await self.handle_clear_message(irc_parameters)
        # HOST TARGET
        elif irc_type == IRCType.HOSTTARGET:
            await self.handle_host_target(irc_parameters)

    # Send twitch user's authentication details and request full capabilities
    async def handshake(self):

        # Send Twitch Authentication
        await self.twitch_irc.send(f'PASS {self.config.oauth_key}')
        await self.twitch_irc.send(f'NICK {self.config.username}')
        await self.twitch_irc.send(f'USER {self.config.username} * * : {self.config.username}')

        # Send Capabilities
        await self.twitch_irc.send('CAP REQ :twitch.tv/commands')
        await self.twitch_irc.send('CAP REQ :twitch.tv/tags')
        await self.twitch_irc.send('CAP REQ :twitch.tv/membership')

    # Find a code from the irc data
    async def expect_code(self, irc_parameters, code):
        for irc in irc_parameters:
            if irc == code: return True
        return False
    
    # Load timers
    def start_timers(self):
        self.logger.info('Starting timers')

        # Event timer
        self.event_timer = RepeatingTimer(1, self.event_tick)
        self.event_timer.start()

    def event_tick(self):
        current_day = int(date.today().strftime('%d'))

        # Reset twitch disconnects after 10
        if self.twitch_disconnects > 5:
            self.twitch_disconnects = 0

        if current_day != self.start_day:
            
            # Fire!
            self.event_handler.on_newday(NewdayEvent())

            # Remove old handlers
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

            # Start new log file            
            self.logger = Log('main').setup_custom_logger()

            self.start_day = current_day

            self.word_handler.channel_word_count.clear()
            self.logger.info('Newday!')

        
        # If reconnect flag is set and we have disconnected from twitch
        if self.reconnect_flag and not self.connected:
            self.logger.warning('Reconnecting')

            # Calculate new exponential backoff time and sleep for duration
            sleep_time = self.calculate_expo_backoff() * 10

            # Fire!
            self.event_handler.on_reconnect(ReconnectEvent(sleep_time))

            # Reset the reconnect flag
            self.reconnect_flag = False

            time.sleep(sleep_time)
            
            # Start a new connect loop
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.connect_to_twitch())            

    # Load configuration 'config.json'
    def load_configurations(self):

        # Configuration name
        config_folder = './data'
        config_name = 'config.json'
        config_path = path.join(config_folder, config_name)

        if not os.path.isdir(config_folder):
            os.mkdir(config_folder)

        # Configuration template
        config_json = """
        {
            "username":"",
            "oauth_key":"",
            "client_id":"",
            "client_secret":"",
            "channels":[],
            "bot_operators":[],
            "command_trigger":"~",
            "influx_db":true,
            "verbose":true
        }
        """
        
        # If config does not exist, make a blank one. Otherwise, open current
        if not path.exists(config_path):
            config_file = open(config_path, 'w')
            config_json_obj = json.loads(config_json)
            
            # prettify!
            formatted_json = json.dumps(config_json_obj, indent=2)
            
            config_file.write(formatted_json)
            config_file.close()
            self.logger.info('config.json was generated in data/config.json\nPlease fill in a username and oauth key')
            os._exit(1)
        else:
            config_file = open(config_path, 'r')
            config_json_obj = json.load(config_file)
                
        self.config = Config(**config_json_obj)

        if not self.config.username or not self.config.oauth_key:
            self.logger.error('Please fill in a username and oauth key')
            exit(1)

    # Load built-in bot commands
    def load_builtin_commands(self):
        pass
        # self.add_command(commands.TestCommand())

    ##############################
    #           Events           #
    ##############################

    # Returns a ping reply with a pong and fires it
    async def handle_pong(self, irc_parameters):
        await self.twitch_irc.send("PONG :tmi.twitch.tv")
        self.event_handler.on_ping(PingEvent())

    # Builds a message event and fires it
    async def handle_message(self, irc_parameters):
        tag = Tag(irc_parameters[0])
        display_name = tag.get('display-name')
        channel = await self.get_channel(irc_parameters[3])
        user = channel.get_user(tag.get('display-name'))

        # Build message
        message = await self.concat_at(4, len(irc_parameters), irc_parameters)
        
        message = message[1:]

        # User has not been seen by the bot yet
        if user is not None:
            user.tag = tag # set the user tag for the private message instance

            # Bot Command
            if str.startswith(message, self.config.command_trigger):
                parameters = ''
            
                # Get command parameters
                if len(irc_parameters) > 5:
                    command_parameters = await self.concat_at(5, len(irc_parameters), irc_parameters)
                    command_parameters = [element.lower() for element in command_parameters]

                
                # Strip command name
                name = str.strip(irc_parameters[4][2:]).lower()

                # Command message and event
                command_message = CommandMessage(name, command_parameters, channel, user, time.time())
                command_event = CommandEvent(user, channel, command_message, self.twitch_irc)

                # Handle built-in commands
                await self.handle_command(command_event)

                # Fire!
                self.event_handler.on_command(command_event)
            # Channel Message
            else:                
                # Build message object
                message_obj = Message(tag.get('id'), message, channel, user, time.time(), tag)
                
                # Handle word
                self.word_handler.handle_message(message_obj)

                # Construct private message event
                privmsg_event = MessageEvent(user, channel, message_obj)
                
                # Fire!
                self.event_handler.on_message(privmsg_event)
        
        # User has spoken prior
        else:
            user = User(display_name)
            user.tag = tag
            channel.add_user(user)

            # Bot Command
            if str.startswith(message, self.config.command_trigger):
                command_parameters = ''
                
                # If parameters were given
                if len(irc_parameters) > 5:
                    command_parameters = await self.concat_at(5, len(irc_parameters), irc_parameters)
                    command_parameters = [element.lower() for element in command_parameters]
                
                # Strip whitespaces and new lines
                name = str.strip(irc_parameters[4][2:]).lower()

                # Build command message and event
                command_message = CommandMessage(name, command_parameters, channel, user, time.time())
                command_event = CommandEvent(user, channel, command_message, self.twitch_irc)

                # Handle built-in commands
                await self.handle_command(command_event)

                # Fire!
                self.event_handler.on_command(command_event)

            # Channel Message
            else:                
                # Build message object
                message_obj = Message(tag.get('id'), message, channel, user, time.time(), tag)

                # Handle word
                self.word_handler.handle_message(message_obj)

                # Construct private message event
                privmsg_event = MessageEvent(user, channel, message_obj)
                
                # Fire!
                self.event_handler.on_message(privmsg_event)

    # Builds a join event and fires it
    async def handle_join(self, data, irc_parameters):
        pd = data.split('!')
        channel = await self.get_channel(irc_parameters[2])
        user = channel.get_user(pd[0][1:])

        # If user has not been identified yet
        if user is None:
            user = User(pd[0][1:])
            channel.add_user(user)

        # Create join event
        join_event = JoinEvent(user, channel)

        # Fire!
        self.event_handler.on_join(join_event)

    # Builds a part event and fires it
    async def handle_part(self, data, irc_parameters):
        pd = data.split('!')
        channel = await self.get_channel(irc_parameters[2])
        user = channel.get_user(pd[0][1:])
        
        # Remove user from channel
        channel.remove_user(pd[0][1:])
        
        # Build event
        part_event = PartEvent(user, channel)

        # Fire!
        self.event_handler.on_part(part_event)

    # Builds a notice event and fires it
    async def handle_notice(self, irc_parameters):
        tag = Tag(irc_parameters[0])
        channel = await self.get_channel(irc_parameters[3])

        try:
            notice_type = NoticeType[tag.get('msg-id').upper()]
        except KeyError as e:
            self.logger.error(f'Notice Type error for {irc_parameters}')
            
        # Build notice message
        notice_message = await self.concat_at(4, len(irc_parameters), irc_parameters)

        # Build event
        notice_event = NoticeEvent(notice_type, channel, tag, notice_message)

        # Fire!
        self.event_handler.on_notice(notice_event)

    # Builds a user notice event and fires it
    async def handle_user_notice(self, irc_parameters):
        tag = Tag(irc_parameters[0])

        # Skip user notices if it's for the bots
        if tag.get('display-name') == self.config.username: return

        channel = await self.get_channel(irc_parameters[3])
        sender = channel.get_user(tag.get('display-name'))
        
        try:
            # Get user notice type from tag
            try:
                user_notice_type = NoticeType[tag.get('msg-id').upper()]
            except KeyError as e:
                self.logger.error(f'User Notice Type error for {irc_parameters}')

            user_notice_message = tag.get('system-msg')

            # If sender has been seen before
            if sender is not None:
                user_notice_event = UserNoticeEvent(user_notice_type, channel, sender, tag, user_notice_message)
                
                # Fire!
                self.event_handler.on_user_notice(user_notice_event)
            else:
                sender = User(tag.get('display-name'))
                channel.add_user(sender)

                user_notice_event = UserNoticeEvent(user_notice_type, channel, sender, tag, user_notice_message)
                
                # Fire!
                self.event_handler.on_user_notice(user_notice_event)
        except(ReferenceError):
            self.logger.error("Error referencing type for USERNOTICE")

    # Builds a user state event and fires it
    async def handle_user_state(self, irc_parameters):
        tag = Tag(irc_parameters[0])
        channel = await self.get_channel(irc_parameters[3])
        
        # Build user event
        user_state_event = UserStateEvent(channel, tag)

        # Fire!
        self.event_handler.on_user_state(user_state_event)
    
    # Builds a room state event and fires it
    async def handle_room_state(self, irc_parameters):
        tag = Tag(irc_parameters[0])
        channel = await self.get_channel(irc_parameters[3])
        channel.tag = tag

        # Build room state event
        room_state_event = RoomStateEvent(channel)

        # Fire!
        self.event_handler.on_room_state(room_state_event)
    
    # Builds a clear message event and fires it
    async def handle_clear_message(self, irc_parameters):
        tag = Tag(irc_parameters[0])
        channel = await self.get_channel(irc_parameters[3])
        user = channel.get_user(tag.get('login'))

        # If user is not seen in channel
        if user is None:
            user = User(tag.get('login'))
            channel.add_user(user)
        
        # Get the message deleted
        deleted_message = await self.concat_at(4, len(irc_parameters), irc_parameters)

         # Build clear message event
        clear_message_event = ClearMessageEvent(user, channel, tag, deleted_message)

        # Fire!
        self.event_handler.on_clear_message(clear_message_event)

    # Builds a host target event and fires it
    async def handle_host_target(self, irc_parameters):
        host_channel = await self.get_channel(irc_parameters[2])
        hosted_channel = await self.get_channel(irc_parameters[3][1:])
        
        # Initalize amount
        amount = 0
        
        # If amount is provided
        if len(irc_parameters) > 4:
            if irc_parameters[4] != '-':
                amount = int(irc_parameters[4])

        # Build host target event
        host_target_event = HostTargetEvent(host_channel, hosted_channel, amount)
        
        # Fire!
        self.event_handler.on_host_target(host_target_event)
    
    # Event Handler
    def event_handler(self):
        return self.event_handler
        
    ##############################
    #          Channels          #
    ##############################

    # Returns a channel if it exists. Otherwise, creates a new one 
    async def get_channel(self, name):
        channel = None
        
        # add channel prefix
        if str.startswith(name, '#') is False:
            name = '#' + name

        # If the list is empty
        if self.channels is None:
            channel = Channel(name)

        # If the channel exists already
        elif name in self.channels:
            return self.channels[name]
            
        # If the channel does not exist
        else:
            channel = Channel(name)
            
        return channel
    
    # Returns a channel if it exists. Otherwise, creates a new one
    def get_channel_noasync(self, name):
        channel = None
        
        # add channel prefix
        if str.startswith(name, '#') is False:
            name = '#' + name

        # If the list is empty
        if self.channels is None:
            channel = Channel(name)

        # If the channel exists already
        elif name in self.channels:
            return self.channels[name]
            
        # If the channel does not exist
        else:
            channel = Channel(name)
            
        return channel
    
    ##############################
    #          Commands          #
    ##############################

    # Handle commands
    async def handle_command(self, command_event):
        command = await self.get_command(command_event.command_message().command())

        if command is not None:
            await command.on_trigger(command_event)

    # Add command
    def add_command(self, command: Command):
        # For each command name, add a seperate instance into the list
        for name in command.names():

            # If command is not yet added
            if name not in self.commands.keys():
                self.commands[name] = command

    # Remove command
    def remove_command(self, command: Command):
        # For each command name, add a seperate instance into the list
        for name in command.names():

            # If command is not yet added
            if name in self.commands.keys():
                del self.commands[name]
    
    # Get a command by name
    async def get_command(self, name) -> Command:
        if name in self.commands.keys():
            return self.commands[name]

    ##############################
    #            Utils           #
    ##############################

    # Covert IRC command to enum type
    async def convert_2_type(self, line) -> IRCType:
        if 'PRIVMSG' in line:
            return IRCType.PRIVMSG
        elif 'JOIN' in line and 'PRIVMSG' not in line:
            return IRCType.JOIN
        elif 'PART' in line and 'PRIVMSG' not in line:
            return IRCType.PART
        elif 'PING' in line and 'PRIVMSG' not in line:
            return IRCType.PING
        elif 'CAP' in line and 'PRIVMSG' not in line:
            return IRCType.CAP
        elif 'USERNOTICE' in line and 'PRIVMSG' not in line:
            return IRCType.USERNOTICE
        elif 'ROOMSTATE' in line and 'PRIVMSG' not in line:
            return IRCType.ROOMSTATE
        elif 'USERSTATE' in line and 'PRIVMSG' not in line:
            return IRCType.USERSTATE
        elif 'CLEARCHAT' in line and 'PRIVMSG' not in line:
            return IRCType.CLEARCHAT
        elif 'CLEARMSG' in line and 'PRIVMSG' not in line:
            return IRCType.CLEARMSG
        elif 'HOSTTARGET' in line and 'PRIVMSG' not in line:
            return IRCType.HOSTTARGET
        elif 'CTCP' in line and 'PRIVMSG' not in line:
            return IRCType.CTCP
        elif 'RECONNECT' in line and 'PRIVMSG' not in line:
            return IRCType.RECONNECT
        elif 'NOTICE' in line and 'PRIVMSG' not in line:
            return IRCType.NOTICE
            
    # Calculate exponetial backoff time for reconnecting
    def calculate_expo_backoff(self):
        return pow(2, self.twitch_disconnects - 1)

    # Concat a subsection of a list
    async def concat_at(self, start, end, data):
        result = ''
        while start < end:
            result += str(data[start]) + " "
            start += 1
        return result

    # Return uptime
    def get_uptime(self):
        time_now = datetime.datetime.now()
        time_passed_twitch = time_now - self.start_time
        time_passed_bot = time_now - self.bot_start_time
        
        return (time_passed_twitch, time_passed_bot)

