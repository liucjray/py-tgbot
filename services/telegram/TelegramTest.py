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
            'sync_cmd': [
                '/gssync', '/gcsync', '/owsync', '/owusync', '/oasync',
                '/phantomsync', '/drawnumberoldsync', '/drawnumbersync'
            ],
            'svn_log_cmd': ['/gs_svn_log_latest'],
            'gtts_cmd': ['/say='],
            'jobs_cmd': ['/job='],
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
        if text == '/oasync':
            self.set_vcs(self.config['VCS']['OA_PATH'])
        if text == '/phantomsync':
            self.set_vcs(self.config['VCS']['PHANTOM_PATH'])
        if text == '/drawnumberoldsync':
            self.set_vcs(self.config['VCS']['DNO_PATH'])
        if text == '/drawnumbersync':
            self.set_vcs(self.config['VCS']['DN_PATH'])
        self.vcs.sync()

    def svn_log(self, text):
        if text == '/gs_svn_log_latest':
            self.set_vcs(self.config['VCS']['GS_PATH'])
            r = self.vcs.get_svn_version_latest()
            svn_log_latest = self.vcs.get_svn_log_by_version(r)
            self.vcs.send_message(svn_log_latest)
