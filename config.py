from collections import namedtuple
import json

class Config(object):

    def __init__(self, username, oauth_key, client_id, client_secret, channels,
                bot_operators, command_trigger, verbose, influx_db):
        self.username = username
        self.oauth_key = oauth_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.channels = channels
        self.bot_operators = bot_operators
        self.command_trigger = command_trigger
        self.verbose = verbose
        self.influx_db = influx_db
