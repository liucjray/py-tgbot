from services.TelegramBase import *
from services.SyncGitSvn import *


class TelegramTest(TelegramBase):
    vcs = None
    chat_id = None
    token = None

    def __init__(self):

        self.token = self.config['TG']['ACCESS_TOKEN_GYOABOT']
        self.chat_id = self.config['TG']['CHAT_ID_TEST']

        settings = {
            'token': self.token,
            'chat_id': self.chat_id,
            'collection': 'test',
            'delete_cmd': ['test', 'del'],
            'sync_cmd': ['/gssync'],
        }
        super(TelegramTest, self).__init__(settings)

    def set_vcs(self):
        settings = {
            'path': self.config['VCS']['GS_PATH'],
            'bot': self.get_bot(),
            'chat_id': self.chat_id,
        }
        self.vcs = SyncGitSvn(settings)

    def vcs_sync(self):
        self.set_vcs()
        self.vcs.sync()
