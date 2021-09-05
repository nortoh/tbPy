class TwitchConnection:

    async def connect(self):
        pass

    async def close(self):
        pass

    async def receive(self) -> str:
        pass

    async def send(self, message):
        pass

    def send_sync(self, message):
        pass