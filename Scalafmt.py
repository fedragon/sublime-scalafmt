import os
import sublime
import sublime_plugin
import subprocess
import time
import functools
import logging

logger = logging.getLogger('SublimeLinter.plugins.scalafmt')

SCALAFMT_CONFIG_FILES = [
    '.scalafmt.conf'
]


class ScalafmtFormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        full_path = self.view.file_name()
        _, file_extension = os.path.splitext(full_path)

        if file_extension == '.scala':
            if not self._is_nailgun_running():
                logger.info('Nailgun is not running')

                if not self._start_nailgun():
                    sublime.error_message('Scalafmt: I am unable to start Nailgun, quitting.')
                    return 1
            else:
                logger.info('Nailgun is up and running')

            if 'TERM' not in os.environ:
                os.environ['TERM'] = 'xterm'

            logger.info('About to format {}'.format(full_path))
            subprocess.call(['ng', 'ng-alias', 'scalafmt', 'org.scalafmt.cli.Cli'])

            config_dir = os.path.abspath(os.path.dirname(full_path))
            config_file = _find_scalafmt_config(config_dir)

            if not config_file:
                config_file = os.path.join(os.path.expanduser('~'), SCALAFMT_CONFIG_FILES[0])

                subprocess.call(['touch', config_file])

            region = sublime.Region(0, self.view.size())
            unformatted = self.view.substr(region)

            logger.info('Using configuration file {}'.format(config_file))

            p = subprocess.Popen(
                ['ng', 'scalafmt',
                 '--config', config_file,
                 '--non-interactive',
                 '--stdin',
                 full_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            outs, errs = p.communicate(unformatted.encode('utf-8'))

            if not errs:
                formatted = outs.decode()

                if not formatted:
                    sublime.status_message('Scalafmt: syntax errors, cannot format')
                elif formatted == unformatted:
                    logger.info('Nothing to do')
                else:
                    self.view.replace(
                        edit,
                        region,
                        formatted)
            else:
                logger.info(errs.decode())

    def _is_nailgun_running(self):
        try:
            subprocess.check_output(['pgrep', '-f', '-x', '^.*scalafmt_ng$'])
            return True
        except Exception:
            return False

    def _start_nailgun(self):
        logger.info('Starting Nailgun ...')

        ready = False

        try:
            subprocess.Popen(['scalafmt_ng'])

            for _ in range(1, 10):
                if not self._is_nailgun_ready():
                    logger.info('Waiting 100ms for Nailgun to start ...')
                    time.sleep(0.1)
                else:
                    ready = True
                    break

            return ready

        except Exception:
            return False

    def _is_nailgun_ready(self):
        try:
            subprocess.check_call(['nc', '-vz', 'localhost', '2113'])
            return True
        except Exception:
            return False


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


@memoize
def _find_scalafmt_config(start_dir, alt_dirs=None):
    dirs = _generate_dirs(start_dir, limit=500)
    for d in dirs:
        for config_file in SCALAFMT_CONFIG_FILES:
            target = os.path.join(d, config_file)
            if os.path.exists(target):
                return target

    if alt_dirs is None:
        alt_dirs = []
    if '~' not in alt_dirs:
        alt_dirs.append('~')

    for d in alt_dirs:
        d = os.path.expanduser(d)
        for config_file in SCALAFMT_CONFIG_FILES:
            target = os.path.join(d, config_file)
            if os.path.exists(target):
                return target

    return None


def _generate_dirs(start_dir, limit=None):
    right = True

    while right and (limit is None or limit > 0):
        yield start_dir
        start_dir, right = os.path.split(start_dir)

        if limit is not None:
            limit -= 1
