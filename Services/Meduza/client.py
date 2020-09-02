import aiohttp

from .tasks import Parser


class Client:
    _SOURCE = 'https://meduza.io/'
    _LIST_URL = 'https://meduza.io/api/w5/screens/news'

    async def get_news_list(self, channel):
        resp = await self.get_page_content()
        news = resp['documents']

        for url, info in news.items():
            if info.get('image') and info['image'].get('elarge_url') and not info.get('affilate'):
                Parser.create_task(
                    rabbit_channel=channel,
                    msg={
                        'url': url,
                        'title': info['title'],
                        'img_url': info['image']['elarge_url']
                    })

    async def get_page_content(self):
        async with aiohttp.ClientSession() as client:
            async with client.get(self._LIST_URL) as resp:
                return await resp.json()
