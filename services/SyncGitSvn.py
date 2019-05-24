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
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        print(output)
        return output

    def sync(self):
        self.eo("svn update")
        self.sync_git()

    def sync_git(self):
        self.eo("git reset --hard")
        self.eo("git clean -df")
        self.eo("git pull")

    def tag_local(self, tag_name, svn_version):
        command = 'git tag -a %s -m "sync svn r%s"' % (
            tag_name, svn_version.strip())
        self.eo(command)

    def tag_remote(self, tag_name):
        command = 'git push origin %s' % tag_name
        self.eo(command)

    def tag(self):
        self.sync()
        tag_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        svn_version = self.eo("svn info --show-item last-changed-revision")
        svn_status = self.eo("svn status")
        git_status = self.eo("git status -s")
        if svn_status == git_status:
            self.tag_local(tag_name, svn_version)
            self.tag_remote(tag_name)
            self.send_tag_msg(tag_name, svn_version)
        else:
            print('### [Error] git svn 目前為非同步狀態 ###')

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
