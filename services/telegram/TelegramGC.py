from services.telegram.TelegramBase import *
from services.vcs.SyncGitSvn import *


class TelegramGC(TelegramBase):
    vcs = None
    chat_id = None
    token = None

    def __init__(self):

        self.chat_id = self.config['TG']['CHAT_ID_GC']
        self.token = self.config['TG']['ACCESS_TOKEN_GYOABOT']

        settings = {
            'token': self.token,
            'chat_id': self.chat_id,
            'collection': 'gc',
            'tag_cmd': ['/gctag'],
        }
        super(TelegramGC, self).__init__(settings)

    def set_vcs(self):
        settings = {
            'path': self.config['VCS']['GC_PATH'],
            'bot': self.get_bot(),
            'chat_id': self.chat_id,
        }
        self.vcs = SyncGitSvn(settings)

    def tag(self):
        self.set_vcs()
        self.vcs.tag()
