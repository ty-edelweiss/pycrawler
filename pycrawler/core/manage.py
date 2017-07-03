#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import logging
from typing import List

from .append import Appender
from .thread import DataGetter, DataMapper

class Scheduler(object):

    def __init__(self):
        """
        This is scheduler model, so become able to set crawling schedule.
        """

    def start(self):
        """
        starting scheduler and this method is overrided absolutely.
        """

    def stop(self):
        """
        stopping scheduler and this method is override absolutely.
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

    def start(self, appenders: List[Appender]):
        start_time = time.time()
        getter = DataGetter(self.queue_)
        mapper = DataMapper(self.queue_, appenders)

        self.running_ = True

        while self.running_:
            self.logger_.info("Crawling scheduler running ... ")
            elapsed_time = time.time() - start_time
            if getter.running_ or mapper.running_:
                time.sleep(self.interval_time_)
            elif elapsed_time >= self.sleep_time_:
                start_time = time.time()
                getter.run()
                mapper.run()
            else:
                time.sleep(self.check_time_)

        self.logger_.info("Crawling scheduler shutdown")


    def stop(self) -> object:
        self.running_ = False