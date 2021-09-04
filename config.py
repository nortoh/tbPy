from collections import namedtuple
import json

class Config(object):

    def __init__(self, username, oauth_key, client_id, client_secret, discord_bot_token, wait_for_live, channels,
                bot_operators, discord_operators, command_trigger, verbose, influx_db, debug):
        self.username = username
        self.oauth_key = oauth_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.discord_bot_token = discord_bot_token
        self.wait_for_live = wait_for_live
        self.channels = channels
        self.bot_operators = bot_operators
        self.discord_operators = discord_operators
        self.command_trigger = command_trigger
        self.verbose = verbose
        self.influx_db = influx_db
        self.debug = debug 