from services.TelegramBase import *


class TelegramTR2(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_TR2'],
            'collection': 'tr2',
            'delete_cmd': ['fuck'],
        }
        super(TelegramTR2, self).__init__(settings)
