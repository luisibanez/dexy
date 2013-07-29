from dexy.utils import file_exists
import dexy.plugin
import os
import shutil

class Reporter(dexy.plugin.Plugin):
    """
    Base class for types of reporter.
    """
    aliases = []
    __metaclass__ = dexy.plugin.PluginMeta

    _settings = {
            "default" : ("Whether to run this report by default. Should be False for reports with side effects.", True),
            "dir" : ("Top-level directory in which report will be stored", None),
            'filename' : ("Name of file to generate (only used if report only generates a single file).", None),
            "in-cache-dir" : ("Whether to write reports in the cache directory (instead of project root).", False),
            'no-delete' : ("List of elements not to delete when resetting report dir (only effective if report dir is cleaned element-wise).", ['.git', '.nojekyll']),
            "run-for-wrapper-states" : ("List of states in which this report can be run.", ["ran"]),
            "readme-filename" : ("Name of README file. Set to None to not have a dexy boilerplate warning README.", "README"),
            "safety-filename" : ("Name of a file which will be created in generated dir, and checked before generated dir is removed.", ".dexy-generated"),
            }
    _UNSET = []

    def is_active(self):
        return True

    def cache_reports_dir(self):
        return os.path.join(self.wrapper.artifacts_dir, "reports")

    def report_dir(self):
        """
        Returns path of report directory relative to dexy project root.
        """
        if not self.setting('dir'):
            return None
        elif self.setting('in-cache-dir'):
            return os.path.join(self.cache_reports_dir(), self.setting('dir'))
        else:
            return self.setting('dir')

    def report_file(self):
        if self.setting('dir'):
            return os.path.join(self.report_dir(), self.setting('filename'))
        else:
            if self.setting('in-cache-dir'):
                return os.path.join(self.cache_reports_dir(), self.setting('filename'))
            else:
                return self.setting('dir')

    def key_for_log(self):
        return "reporter:%s" % self.aliases[0]

    def log_debug(self, message):
        self.wrapper.log.debug("%s: %s" % (self.key_for_log(), message))

    def log_info(self, message):
        self.wrapper.log.info("%s: %s" % (self.key_for_log(), message))

    def log_warn(self, message):
        self.wrapper.log.warn("%s: %s" % (self.key_for_log(), message))

    def safety_filepath(self):
        return os.path.join(self.report_dir(), self.setting('safety-filename'))

    def readme_filepath(self):
        if self.setting('readme-filename'):
            return os.path.join(self.report_dir(), self.setting('readme-filename'))

    def write_safety_file(self):
        with open(self.safety_filepath(), "w") as f:
            f.write("""
            This directory was generated by the %s Dexy Reporter and
            may be deleted without notice.\n\n""" % self.__class__.__name__)

    def write_readme_file(self):
        with open(self.readme_filepath(), "w") as f:
            f.write("""
            This directory was generated by the %s Dexy Reporter and
            may be deleted without notice.\n\n""" % self.__class__.__name__)

    def create_cache_reports_dir(self):
        if not file_exists(self.cache_reports_dir()):
            os.makedirs(self.cache_reports_dir())

    def create_reports_dir(self):
        if not self.report_dir():
            return False

        if not file_exists(self.report_dir()):
            os.makedirs(self.report_dir())

        self.write_safety_file()
        if self.readme_filepath():
            self.write_readme_file()

    def remove_reports_dir(self, keep_empty_dir=False):
        if not self.report_dir():
            return False

        if file_exists(self.report_dir()) and not file_exists(self.safety_filepath()):
            msg = "Please remove directory %s, Dexy wants to write a report here but there's already a file or directory in this location."
            msgargs = (os.path.abspath(self.report_dir()),)
            raise dexy.exceptions.UserFeedback(msg % msgargs)
        elif file_exists(self.report_dir()):
            if keep_empty_dir:
                # Does not remove the base directory, useful if you are running
                # a process (like 'dexy serve') from inside that directory
                for f in os.listdir(self.report_dir()):
                    if not f in self.setting('no-delete'):
                        path = os.path.join(self.report_dir(), f)
                        if os.path.isdir(path):
                            shutil.rmtree(path)
                        else:
                            os.remove(path)
                self.write_safety_file()
            else:
                shutil.rmtree(self.report_dir())

    def run(self, wrapper):
        pass
