# coding: utf-8
import sys
import chardet
import subprocess
import time


class SyncGitSvn:
    path = None
    bot = None
    chat_id = None

    def __init__(self, settings):
        self.path = settings['path']
        self.bot = settings['bot']
        self.chat_id = settings['chat_id']

    def e(self, command):
        command = "cd %s & %s" % (self.path, command)
        subprocess.check_output(command, shell=True).decode('utf-8')

    def eo(self, command):
        command = "cd {} & {}".format(self.path, command)
        print(command)
        output = subprocess.check_output(command, shell=True)

        if chardet.detect(output) is not None:
            encodeing = chardet.detect(output)['encoding']
            if encodeing is not None:
                output = output.decode(encodeing).encode('utf-8')

        return output.decode('utf-8')

    def sync(self):
        self.eo("svn revert -R .")
        self.eo("svn update")
        self.sync_git()
        self.bot.send_message(self.chat_id, 'sync success')

    def sync_git(self):
        self.eo("git reset --hard")
        self.eo("git clean -df")
        self.eo("git pull")

    def tag_local(self, tag_name, svn_version):
        command = 'git tag -a %s -m "sync svn r%s"' % (tag_name, svn_version.strip())
        self.eo(command)

    def tag_remote(self, tag_name):
        command = 'git push origin %s' % tag_name
        self.eo(command)

    def tag(self):
        self.sync()
        tag_name = time.strftime("%Y%m%d", time.localtime())
        svn_version = self.get_svn_version_latest()
        svn_status = self.eo("svn status")
        git_status = self.eo("git status -s")
        if svn_status == git_status:
            if self.tag_local_check(tag_name):
                self.tag_local(tag_name, svn_version)
                self.tag_remote(tag_name)
                self.send_tag_msg(tag_name, svn_version)
            else:
                error_msg = '### [Error] git tag (%s) 已存在 ###' % tag_name
                self.send_message(error_msg)
                print(error_msg)
        else:
            error_msg = '### [Error] git svn 目前為非同步狀態 ###'
            self.send_message(error_msg)
            print(error_msg)

    def get_svn_version_latest(self):
        # 先執行一次更新避免未讀取到最新版號
        self.e("svn update")

        command = "svn info --show-item last-changed-revision"
        return self.eo(command)

    def get_svn_log_by_version(self, version):
        command = "svn log -v -c {}".format(version)
        return self.eo(command)

    def tag_local_check(self, tag_name):
        command = "git tag -l %s" % tag_name
        msg = self.eo(command)
        if msg == "":
            return True
        return False

    def tag_local_delete(self, tag_name):
        command = "git push --delete origin %s" % tag_name
        self.eo(command)

    def tag_remote_delete(self, tag_name):
        command = "git tag --delete %s" % tag_name
        self.eo(command)

    def tag_clean(self, tag_name):
        self.tag_local_delete(tag_name)
        self.tag_remote_delete(tag_name)

    def hub_master(self):
        self.eo("git checkout master")
        self.eo("git reset --hard")
        self.eo("git clean -df")
        self.eo("git pull")
        self.eo("git push hub master")

    def hub_release(self):
        self.eo("git checkout release")
        self.eo("git reset --hard")
        self.eo("git clean -df")
        self.eo("git pull")
        self.eo("git push hub release")

    def send_tag_msg(self, tag_name, svn_version):
        msg = "GIT release & master => TAG %s = SVN r%s\n#tag" % (tag_name, svn_version)
        self.bot.send_message(self.chat_id, msg)

    def send_message(self, msg):
        self.bot.send_message(self.chat_id, msg)

#
# vcs = SyncGitSvn({'path': 'C:\B2B\gameserver.SVN', 'bot': None, 'chat_id': None})
# v = vcs.get_svn_version_latest()
# log = vcs.get_svn_log_by_version(v)
# print(log)
