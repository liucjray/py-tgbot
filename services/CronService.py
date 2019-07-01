import time
from bson.objectid import ObjectId
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

    def get_jobs(self, chat_id=None):
        # 預設搜尋條件: 未發訊息 & 未來訊息
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        where = {"cron.done": 0, "cron.time": {"$gt": now}}

        if chat_id is None:
            jobs = self.atlas.find(where)
        else:
            where["message.chat.id"] = int(chat_id)
            jobs = self.atlas.find(where)

        return jobs.sort('cron.time', -1)

    def del_job(self, _id=None):
        if _id is not None:
            update = {"$set": {"cron.done": 1}}
            where = {"_id": ObjectId(_id)}
            self.atlas.update(where=where, update=update)

    def exec(self):
        for job in self.get_jobs():
            chat_id = job.get('message', {}).get('chat', {}).get('id', None)
            text = job.get('cron', {}).get('text', None)

            if chat_id and text:
                bot = TelegramBot({}).get_bot()
                bot.send_message(chat_id, text)
            else:
                print('[Invalid] chat_id:{} text:{}'.format(chat_id, text))
