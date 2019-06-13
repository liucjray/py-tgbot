import time
import telegram
from repositories.AtlasService import *
from services.AioHttpService import *
from services.google.GttsService import *
from services.CronService import *
from helpers.Common import *


class TelegramBase:
    config = get_config()
    bot = aiohttp = None
    token = chat_id = None
    prepares = []
    delete_prepares = []
    is_webhook_set = False

    def __init__(self, settings):
        # attr
        self.token = settings['token']
        self.chat_id = settings['chat_id']
        self.collection = settings['collection']

        # attr cmd
        self.delete_cmd = settings.get('delete_cmd', ['000'])
        self.tag_cmd = settings.get('tag_cmd', None)
        self.sync_cmd = settings.get('sync_cmd', None)
        self.gtts_cmd = settings.get('gtts_cmd', None)
        self.jobs_cmd = settings.get('jobs_cmd', None)

        # mongodb
        self.atlas = AtlasService(settings)

        # telegram bot
        self.set_bot()
        # self.check_is_webhook_set()

        # async request
        self.aiohttp = AioHttpService()

        # Google gtts
        self.gtts = GttsService(self.config)

        # cron
        self.cron = CronService({"chat_id": settings['chat_id']})

        self.bot2 = TelegramBot({})

    def set_bot(self):
        self.bot = telegram.Bot(token=self.token)

    def get_bot(self):
        if self.bot is None:
            self.set_bot()
        return self.bot

    def get_updates(self):
        return self.bot.get_updates()

    def write(self):
        return self.atlas.write(self.get_updates())

    def write_by_webhook(self, update):
        updates = [update]
        self.atlas.write(updates)

    def delete_prepare(self):
        a = get_caller(show=True)
        for r in self.atlas.get_data_exist():
            # before delete
            text = r.get('message.text') if 'message.text' in r else 'Not text or not exist.'
            is_deleted = r.get('is_deleted') if 'is_deleted' in r else 0
            if int(is_deleted) == 1:
                print('text: [' + text + '] has been deleted.')
                continue

            # prepare list of delete
            d = {
                # 'update_id': r['update_id'],
                'chat_id': r['message']['chat']['id'],
                'message_id': r['message']['message_id'],
            }
            d['url'] = self.bot2.build_delete_url(d)
            self.delete_prepares.append(d)

    def delete_exec(self):
        t1 = time.time()
        if self.delete_prepares:
            # telegram delete requests
            results = self.aiohttp.handler(self.delete_prepares)

            # database update delete rows (success / not found)
            for d in results:
                if d and d.get('message_id'):
                    message_id = d.get('message_id', 0)
                    self.atlas.delete(where={'message.message_id': int(message_id)}, update={'$set': {'is_deleted': 1}})
        print("Async delete total time:", time.time() - t1)

    def delete(self):
        self.delete_prepare()
        self.delete_exec()

    def read(self):
        return self.atlas.read()

    def check_is_webhook_set(self):
        json = self.bot.get_webhook_info()
        r = isinstance(json['url'], str)
        self.is_webhook_set = r

    def set_webhook(self):
        return self.bot2.set_webhook()

    def listen_webhook(self, dict_update):
        self.write_by_webhook(dict_update)

        text = dict_update.get('message', {}).get('text', None)
        chat_id = dict_update.get('message', {}).get('chat', {}).get('id', 0)

        # 驗證 chat_id
        if int(chat_id) == int(self.chat_id) and text is not None:
            # 檢查是否有刪除關鍵字
            if text in self.delete_cmd:
                self.delete()

            # 檢查是否有 tag 關鍵字
            if self.tag_cmd is not None:
                if text in self.tag_cmd:
                    self.tag()

            # 檢查是否有 sync 關鍵字
            if self.sync_cmd is not None:
                if text in self.sync_cmd:
                    self.vcs_sync(text)

            # 檢查是否有 ttx 關鍵字
            if self.gtts_cmd is not None:
                if text[0:len(self.gtts_cmd[0])] == self.gtts_cmd[0]:
                    new_text = text[len(self.gtts_cmd[0]):len(text)]
                    file_path = self.get_gtts_audio(new_text)
                    r = self.bot2.send_audio(chat_id, file_path)

                    # bot 訊息發後須寫入訊息，之後才刪的到
                    u = self.bot2.format_send_audio_message_resp(r)
                    self.write_by_webhook(u)

            # 檢查 jobs 關鍵字
            if self.jobs_cmd is not None:
                if text[0:len(self.jobs_cmd[0])] == self.jobs_cmd[0]:
                    self.add_job(dict_update, text)

    def send_message(self, message):
        self.bot2.send_message(self.chat_id, message)

    def get_gtts_audio(self, text, lang=''):
        return self.gtts.get_file(text, lang)

    def add_job(self, updates, text):
        # todo: 驗證輸入格式 text
        # format /job=text,time
        j_text = text[len(self.jobs_cmd[0]): text.find('|')]
        j_time = text[text.find('|') + 1: len(text)]

        sample_time = '20190102030405'
        if len(j_time) == len(sample_time) and j_time.isdigit():
            job = {"cron": {"text": j_text, "time": j_time, "done": 0}}
            self.cron.add(updates, job)
            msg = '[O] 定時任務新增成功\n===================\n時間: {}\n訊息: {}'.format(j_time, j_text)
        else:
            msg = '[X] 定時任務新增失敗'

        # 回傳加入排程資訊
        r = self.bot2.send_message(self.chat_id, msg)

        # bot 訊息發後須寫入訊息，之後才刪的到
        u = self.bot2.format_send_message_resp(r)
        self.write_by_webhook(u)

