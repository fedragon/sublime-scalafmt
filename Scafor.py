import os
import sublime
import sublime_plugin
import subprocess
import sys
import time

class FormatScalaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        full_path = self.view.file_name()
        _, file_extension = os.path.splitext(full_path)

        if file_extension == '.scala':
            if not self._is_nailgun_running():
                print('Nailgun is not running')

                try:
                    if not self._start_nailgun():
                        sublime.error_message('Format Scala: I cannot start Nailgun!')
                        return 1
                except:
                  sublime.error_message('WTF')
                  return 1
            else:
                print('Nailgun is up and running')

            print('About to format ' + full_path)
            subprocess.call(['ng', 'ng-alias', 'scalafmt', 'org.scalafmt.cli.Cli'])

            p = subprocess.Popen(\
                ['ng', 'scalafmt', \
                 '--config', os.path.expanduser("~") + '/.scalafmt.conf', \
                 '--non-interactive', \
                 '--stdout', \
                 full_path], \
                 stdout = subprocess.PIPE,
                 stderr = subprocess.PIPE).communicate()

            self.view.replace(\
                edit, \
                sublime.Region(0, self.view.size()), \
                p[0].decode())

    def _is_nailgun_running(self):
        try:
            subprocess.check_output(['pgrep', '-f', '-x', '^.*scalafmt_ng$'])
            True
        except:
            False

    def _start_nailgun(self):
        print('Starting Nailgun ...')

        ready = False

        try:
            subprocess.Popen(["scalafmt_ng"])

            for _ in range(1, 10):
                if not self._is_nailgun_ready:
                    time.sleep(0.1)
                else:
                    ready = True
                    break

            return ready
        except:
            False

    def _is_nailgun_ready(self):
        try:
            subprocess.check_call(['nc', '-vz', 'localhost', '2113'])
            True
        except:
            print('nailgun is NOT ready')
            False
