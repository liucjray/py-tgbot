import asyncio
import aiohttp
import json
from helpers import UrlParser


class AioHttpService:
    results = []

    def handler(self, dataset):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main(loop, dataset))
        loop.close()
        return self.results

    async def job(self, session, url):
        result = {"chat_id": "", "message_id": "", "url": ""}
        response = await session.get(url)  # 等待并切换
        body = await response.read()
        body_dict = json.loads(s=body)
        result['url'] = url
        result['chat_id'] = UrlParser.get_qs(url, 'chat_id', None)
        result['message_id'] = UrlParser.get_qs(url, 'message_id', None)
        result = {**result, **body_dict}
        return result

    async def main(self, loop, todos):
        async with aiohttp.ClientSession() as session:  # 官网推荐建立 Session 的形式
            tasks = []
            for todo in todos:
                url = todo['url']
                j = loop.create_task(self.job(session, url))
                tasks.append(j)
            finished, unfinished = await asyncio.wait(tasks)
            self.results = [r.result() for r in finished]
