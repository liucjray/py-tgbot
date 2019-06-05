import time
import telegram
from repositories.AtlasService import *
from services.AioHttpService import *


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

        # mongodb
        self.atlas = AtlasService(settings)

        # telegram bot
        self.set_bot()
        self.check_is_webhook_set()

        # async request
        self.aiohttp = AioHttpService()

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
        for r in self.atlas.get_data_exist():
            # before delete
            text = r.get('message.text') if 'message.text' in r else 'Not text or not exist.'
            is_deleted = r.get('is_deleted') if 'is_deleted' in r else 0
            if int(is_deleted) == 1:
                print('text: [' + text + '] has been deleted.')
                continue

            # prepare list of delete
            d = {
                'update_id': r['update_id'],
                'chat_id': r['message']['chat']['id'],
                'message_id': r['message']['message_id'],
            }
            d['url'] = self.build_delete_url(d)
            self.delete_prepares.append(d)

    def build_delete_url(self, delete_dict):
        url = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}'.format(
            self.token,
            delete_dict['chat_id'],
            delete_dict['message_id'],
        )
        return url

    def delete_exec(self):
        t1 = time.time()
        if self.delete_prepares:
            # telegram delete requests
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.aiohttp.main(loop, self.delete_prepares))
            loop.close()

            # database update delete rows
            for d in self.delete_prepares:
                update_id = d['update_id']
                self.atlas.delete(where={'update_id': update_id}, update={'$set': {'is_deleted': 1}})
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
        listen_webhook_url = '/'.join([self.config['NGROK']['URL'], 'listen_webhook'])
        b = self.bot.set_webhook(url=listen_webhook_url)
        msg = "[{}] telegram set_webhook url: {}".format(str(b), listen_webhook_url)
        return msg

    def listen_webhook(self, dict_update):
        self.write_by_webhook(dict_update)

        text = dict_update.get('message', {}).get('text', None)
        chat_id = dict_update.get('message', {}).get('chat', {}).get('id', 0)

        # 驗證 chat_id
        if int(chat_id) == int(self.chat_id):
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

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)
