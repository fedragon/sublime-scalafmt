import os
import sublime
import sublime_plugin
import subprocess
import sys
import time

class ScaforFormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        full_path = self.view.file_name()
        _, file_extension = os.path.splitext(full_path)

        if file_extension == '.scala':
            if not self._is_nailgun_running():
                print('Nailgun is not running')

                try:
                    if not self._start_nailgun():
                        sublime.error_message('ScaFor: I am unable to start Nailgun, quitting.')
                        return 1
                except:
                  sublime.error_message('ScaFor: Something went wrong, quitting.')
                  return 1
            else:
                print('Nailgun is up and running')

            print('About to format ' + full_path)
            subprocess.call(['ng', 'ng-alias', 'scalafmt', 'org.scalafmt.cli.Cli'])

            config_file = os.path.expanduser("~") + '/.scalafmt.conf'

            subprocess.call(['touch', config_file])

            region = sublime.Region(0, self.view.size())
            unformatted = self.view.substr(region)

            p = subprocess.Popen(
                ['ng', 'scalafmt',
                 '--config', config_file,
                 '--non-interactive',
                 '--stdin',
                 full_path],
                 stdin = subprocess.PIPE,
                 stdout = subprocess.PIPE,
                 stderr = subprocess.PIPE)

            formatted = p.communicate(unformatted.encode('utf-8'))[0].decode()

            if not formatted:
                sublime.status_message('ScaFor: syntax errors, cannot format')
            elif formatted == unformatted:
                print('Nothing to do')
            else:
                self.view.replace(
                    edit,
                    region,
                    formatted)

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
            False
