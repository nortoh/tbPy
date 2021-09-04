from commands.command import Command

class LeaveCommand(Command):

    def __init__(self, twitch_bot):
        super().__init__('leave')
        self.twitch_bot = twitch_bot

    async def on_trigger(self, command_event):
        user = command_event.user()
        channel = command_event.channel()
        command_message = command_event.command_message()
        parameters = command_message.parameters()

        channel_provided = False
        channel_parting = channel.name()

        # If a channel is provided
        if len(parameters) > 1:
            channel_provided = True
            channel_parting = self.format_chan(parameters).strip()

        # User is a broadcaster
        if user.is_broadcaster():

            # Leave the channel
            await self.leave_channel(channel_parting, command_event)

        # User is a moderator
        elif user.is_moderator():

            # Channel must be provided
            if not channel_provided:
                await command_event.twitch_irc().send_message(command_event.channel(), f'Missing argument!')
                return

            # Leave the channel
            await self.leave_channel(channel_parting, command_event)

    async def leave_channel(self, name, command_event):

        # If bot is already ignoring channel, do nothing
        if name in self.twitch_bot.channels_ignored_list:
            await command_event.twitch_irc().send_message(command_event.channel(), f'Already ignored!')
            return

        # If channel has been crawled, then we know it is capable of joining a user's channel
        if name in self.twitch_bot.channels_crawled_list:

            # Add to ignore list
            self.twitch_bot.channels_ignored_list.append(name)

            # Set channel to ignored
            self.twitch_bot.set_ignored(name)

            # If we are currently joined in that channel, remove it
            if name in self.twitch_bot.channels_joined_list:

                del self.twitch_bot.channels_joined_list[name]

            await command_event.twitch_irc().send_message(command_event.channel(), f'Ignoring!')

            # Part channel
            self.twitch_bot.twitch_irc.part_channel_noasync(name)
        else:
            await command_event.twitch_irc().send_message(command_event.channel(), f'Did not find!')

    def format_chan(self, name):
        if str.startswith(name, '#'):
            return name
        return f'#{name}'