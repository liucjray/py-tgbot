from services.telegram.TelegramBase import *


class TelegramRABBYWORK(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_RABBYWORK'],
            'collection': 'rabbywork',
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramRABBYWORK, self).__init__(settings)
