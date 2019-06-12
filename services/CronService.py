from repositories.AtlasService import *
from services.telegram.TelegramBot import *


class CronService:
    # 指定 collection
    collection = {'collection': 'cron'}
    config = get_config()

    def __init__(self, settings={}):
        # 資料合併
        settings = {**settings, **self.collection}
        self.atlas = AtlasService(settings)

    def add(self, update=None, job=None):
        if update and job:
            cron = {**update, **job}
            self.atlas.write(cron)

    def get_jobs(self):
        where = {"cron.done": 0}

        # 取出待執行的任務
        jobs = self.atlas.find(where)
        return jobs

    def exec(self):
        for job in self.get_jobs():
            chat_id = job.get('message', {}).get('chat', {}).get('id', None)
            text = job.get('cron', {}).get('text', None)

            if chat_id and text:
                bot = TelegramBot({}).get_bot()
                bot.send_message(chat_id, text)
            else:
                print('[Invalid] chat_id:{} text:{}'.format(chat_id, text))
