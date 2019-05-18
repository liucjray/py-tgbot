import telegram
from services.AtlasService import *


class TelegramBase:
    config = get_config()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    bot = None
    token = None
    chat_id = None
    prepares = []

    def __init__(self, settings):
        self.settings = settings
        self.token = settings['token']
        self.chat_id = settings['chat_id']
        self.collection = settings['collection']
        self.set_bot()
        self.atlas = AtlasService(self.settings)

    def set_bot(self):
        self.bot = telegram.Bot(token=self.token)

    def get_bot(self):
        if self.bot is None:
            self.set_bot()
        return self.bot

    def get_updates(self):
        return self.bot.get_updates()

    def write_prepare(self):
        for update in self.get_updates():
            if int(update.message.chat.id) == int(self.chat_id):
                row = update.to_dict()
                self.prepares.append(row)

    def write(self):
        return self.atlas.write(self.get_updates())

    def delete(self):
        for r in self.atlas.get_data_deleted():
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
