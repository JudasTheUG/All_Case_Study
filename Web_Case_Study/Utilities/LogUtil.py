import logging
import time
import os


class ReplaceSensitiveInformation(logging.Formatter):

    reduction_list = []

    def _filter(self, s):
        for item in self.reduction_list:
            if item.upper() in s.upper():
                s = s.replace(item, "*** ")
        return s

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)


class Logger:

    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        fmt = '%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s'

        curr_time = time.strftime("%Y-%m-%d")
        self.LogFileName = 'log' + curr_time + '.txt'
        if os.path.exists(os.getcwd() + "/Logs"):
            self.LogFileName = os.getcwd() + '/' + 'Logs' + '/' + 'log' + curr_time + '.txt'
        else:
            os.mkdir(os.getcwd() + "/Logs")
            self.LogFileName = os.getcwd() + '/' + 'Logs' + '/' + 'log' + curr_time + '.txt'
        # "a" to append the logs in same file, "w" to generate new logs and delete old one
        fh = logging.FileHandler(self.LogFileName, mode="a+")
        fh.setFormatter(ReplaceSensitiveInformation(fmt))
        fh.setLevel(file_level)
        self.logger.addHandler(fh)
