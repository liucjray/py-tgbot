from services.telegram.TelegramBase import *
from services.vcs.SyncGitSvn import *


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
            'delete_cmd': ['/del'],
            'sync_cmd': ['/gssync', '/gcsync', '/owsync', '/owusync'],
        }
        super(TelegramTest, self).__init__(settings)

    def set_vcs(self, path):
        settings = {
            'path': path,
            'bot': self.get_bot(),
            'chat_id': self.chat_id,
        }
        self.vcs = SyncGitSvn(settings)

    def vcs_sync(self, text):
        if text == '/gssync':
            self.set_vcs(self.config['VCS']['GS_PATH'])
        if text == '/gcsync':
            self.set_vcs(self.config['VCS']['GC_PATH'])
        if text == '/owsync':
            self.set_vcs(self.config['VCS']['OW_PATH'])
        if text == '/owusync':
            self.set_vcs(self.config['VCS']['OWU_PATH'])
        self.vcs.sync()