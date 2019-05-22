from services.TelegramBase import *


class TelegramTest(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_TEST'],
            'collection': 'test',
            'delete_cmd': ['test', 'del'],
        }
        super(TelegramTest, self).__init__(settings)
