from services.telegram.TelegramBase import *


class TelegramRABBY(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_RABBY'],
            'collection': 'rabby',
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramRABBY, self).__init__(settings)
