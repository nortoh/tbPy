import logging
from bot import Bot

class Main(Bot):
    
    """ 
    Main Constructor
    """
    def __init__(self):
        super().__init__()
        
        self.logger = logging.getLogger('main')
        
        # Subscribe to some events
        self.event_handler.on_message += self.on_message

    # Start the bot
    def start(self):
        try:
            self.start_bot()
        except Exception as e:
            self.logger.error(f'Main exception: {e.args}')

    ##############################
    #           Events           #
    ##############################
    
    # On Message Event
    def on_message(self, event_args):
        message = event_args.message().text().strip()
        user = event_args.user().name()
        
# Main method
if __name__ == "__main__":
    main = Main()
    main.start()