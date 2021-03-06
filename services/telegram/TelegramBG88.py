from services.telegram.TelegramBase import *


class TelegramBG88(TelegramBase):
    def __init__(self):
        settings = {
            'token': self.config['TG']['ACCESS_TOKEN_GYOABOT'],
            'chat_id': self.config['TG']['CHAT_ID_BG88'],
            'collection': 'bg88',
            'delete_cmd': ['000', 'BZ', 'bz', '/000'],
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
        }
        super(TelegramBG88, self).__init__(settings)
