from services.telegram.TelegramBase import *


class TelegramRABBYTW(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_STR87WEBHOOKBOT'],
            'chat_id': self.config['TG']['CHAT_ID_RABBY_TW'],
            'collection': 'rabbytw',
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramRABBYTW, self).__init__(settings)
