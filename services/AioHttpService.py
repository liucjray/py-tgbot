import asyncio
import aiohttp


class AioHttpService:

    async def job(self, session, url):
        response = await session.get(url)  # 等待并切换
        # print(response)
        return str(response.url)

    async def main(self, loop, todos):
        async with aiohttp.ClientSession() as session:  # 官网推荐建立 Session 的形式
            tasks = []
            for todo in todos:
                url = todo['url']
                j = loop.create_task(self.job(session, url))
                tasks.append(j)
            finished, unfinished = await asyncio.wait(tasks)
            all_results = [r.result() for r in finished]  # 获取所有结果
            # print(all_results)

# a = AioHttpService()
# t1 = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(a.main(loop))
# loop.close()
# print("Async total time:", time.time() - t1)
