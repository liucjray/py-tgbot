from services.telegram.TelegramBase import *


class TelegramTEAM(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_TEAM'],
            'collection': 'team',
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramTEAM, self).__init__(settings)
