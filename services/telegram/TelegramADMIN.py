from services.telegram.TelegramBase import *


class TelegramADMIN(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_ADMIN'],
            'collection': 'admin',
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramADMIN, self).__init__(settings)
