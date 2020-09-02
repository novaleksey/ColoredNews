from .client import Client


class MeduzaHandler:
    def __init__(self):
        self._client = Client()

    async def handle_scanner(self, task, channel):
        return await self._client.get_news_list(channel)

    def handle_parser(self, task, channel):
        pass