import telegram
from repositories.AtlasService import *


class TelegramBase:
    config = get_config()
    bot = None
    token = None
    chat_id = None
    prepares = []
    is_webhook_set = False

    def __init__(self, settings):
        # attr
        self.delete_cmd = settings.get('delete_cmd', ['000'])
        self.token = settings['token']
        self.chat_id = settings['chat_id']
        self.collection = settings['collection']

        # mongodb
        self.atlas = AtlasService(settings)

        # telegram bot
        self.set_bot()
        self.check_is_webhook_set()

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

    def delete(self):
        for r in self.atlas.get_data_exist():
            # before delete
            text = r.get('message.text') if 'message.text' in r else 'Not text or not exist.'
            is_deleted = r.get('is_deleted') if 'is_deleted' in r else 0
            if int(is_deleted) == 1:
                print('text: [' + text + '] has been deleted.')
                continue

            # delete telegram message
            update_id = r['update_id']
            chat_id = r['message']['chat']['id']
            message_id = r['message']['message_id']
            try:
                b = self.bot.delete_message(chat_id, message_id)
                # 删除成功
                if b is True:
                    self.atlas.delete(where={'update_id': update_id}, update={'$set': {'is_deleted': 1}})
            except Exception as e:
                # 刪除失敗
                self.atlas.delete(where={'update_id': update_id}, update={'$set': {'is_deleted': 1}})
                print(str(e) + '... message_id: ' + str(message_id))

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

        # 檢查是否有刪除關鍵字
        text = dict_update.get('message', {}).get('text', None)
        if text in self.delete_cmd:
            self.delete()

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)
