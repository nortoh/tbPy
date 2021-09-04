import asyncio
import logging
from bot import Bot
from commands.leave_command import LeaveCommand

class Main(Bot):
    
    """ 
    Main Constructor
    """
    def __init__(self):
        super().__init__()
        
        self.logger = logging.getLogger('main')
        
        # Add commands
        self.add_command(LeaveCommand(self))
        
        # Do things
        self.subscribe_events()

    def start_application(self):
        self.loop = asyncio.new_event_loop()
        result = self.loop.run_until_complete(self.start())

    # Start the bot
    async def start(self):
        try:
            await self.start_bot()
        except Exception as e:
            self.logger.error(f'Main exception: {e.args}')

    # Subscribe to events
    def subscribe_events(self):
        self.event_handler.on_message += self.on_message

    ##############################
    #           Events           #
    ##############################
    
    # On Message Event
    def on_message(self, event_args):
        message = event_args.message().text().strip()
        user = event_args.user().name().lower()
        
# Main method
if __name__ == "__main__":
    main = Main()
    main.start_application()