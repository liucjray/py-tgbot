import json
import telegram
from config.config import *


class TelegramBot:
    debug = True
    bot = None
    config = get_config()
    is_webhook_set = False

    def __init__(self, settings):
        self.token = settings.get('token', None) or self.config['TG']['ACCESS_TOKEN_GYOABOT']
        self.set_bot(self.token)

    def set_bot(self, token):
        token = token or self.token
        self.bot = telegram.Bot(token=token)
        return self

    def get_bot(self):
        self.bot = telegram.Bot(token=self.token)
        return self.bot

    def send_message(self, chat_id, text):
        return self.bot.send_message(chat_id, text)

    def send_audio(self, chat_id, file_path):
        if not os.path.exists(file_path):
            raise RuntimeError('File not exists.')
        r = self.bot.send_audio(chat_id, audio=open(file_path, 'rb'))
        return r

    def build_delete_url(self, delete_dict):
        self.msg('bot2.build_delete_url')
        url = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}'.format(
            self.token,
            delete_dict['chat_id'],
            delete_dict['message_id'],
        )
        return url

    def check_is_webhook_set(self):
        j = self.bot.get_webhook_info()
        r = isinstance(j['url'], str)
        self.is_webhook_set = r
        return r

    def set_webhook(self):
        listen_webhook_url = '/'.join([self.config['NGROK']['URL'], 'listen_webhook'])
        b = self.bot.set_webhook(url=listen_webhook_url)
        msg = "[{}] telegram set_webhook url: {}".format(str(b), listen_webhook_url)
        return msg

    def msg(self, msg):
        self.debug and print(msg)

    def format_send_audio_message_resp(self, resp):
        r = {
            "update_id": resp['message_id'],
            "message": {
                "message_id": resp['message_id'],
                "chat": {
                    "id": resp['chat']['id'],
                },
            },
        }
        return r

    def format_send_message_resp(self, resp):
        r = {
            "update_id": resp['message_id'],
            "message": {
                "message_id": resp['message_id'],
                "chat": {
                    "id": resp['chat']['id'],
                },
            },
        }
        return r
