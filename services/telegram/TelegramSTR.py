from services.telegram.TelegramBase import *


class TelegramSTR(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_STR'],
            'collection': 'str',
            'delete_cmd': ['/del'],
        }
        super(TelegramSTR, self).__init__(settings)
