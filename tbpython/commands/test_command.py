from . import Command

class TestCommand(Command):

    def __init__(self):
        super().__init__(['test', 'testing'])

    async def on_trigger(self, command_event):
        pass
        # await command_event.twitch_irc().send_message(command_event.channel(), "Hello")