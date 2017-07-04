#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import logging
from typing import List

from .access import Accessor
from .append import Appender
from .thread import DataGetter, DataMapper

class Scheduler(object):

    def __init__(self, *args, **kwrds):
        """
        This is scheduler model, so become able to set crawling schedule.
        """

    def start(self, *args, **kwrds):
        """
        starting scheduler and this method is overrided absolutely.
        """

    def stop(self, *args, **kwrds):
        """
        stopping scheduler and this method is overrided absolutely.
        """

class TimeScheduler(Scheduler):

    def __init__(self, sleep_time: int = 86400, check_time: int = 3600, interval_time: int = 1):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = queue.Queue()
        self.sleep_time_ = sleep_time
        self.check_time_ = check_time
        self.interval_time_ = interval_time
        self.running_ = False

    def start(self, accessor: Accessor, appenders: List[Appender], **kwrds):
        start_time = time.time()
        self.running_ = True

        end_flag = False
        getter = DataGetter(self.queue_, end_flag, **kwrds)
        mapper = DataMapper(self.queue_, end_flag, **kwrds)
        getter.run(accessor)
        mapper.run(appenders)

        while self.running_:
            self.logger_.info("Crawling scheduler running ... ")
            elapsed_time = time.time() - start_time
            if getter.running_ or mapper.running_:
                time.sleep(self.interval_time_)
            elif elapsed_time >= self.sleep_time_:
                start_time = time.time()
                getter.run(accessor)
                mapper.run(appenders)
            else:
                time.sleep(self.check_time_)

        self.logger_.info("Crawling scheduler shutdown")

    def stop(self) -> object:
        self.running_ = False