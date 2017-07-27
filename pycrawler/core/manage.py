#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import logging
from typing import List

from .access import Accessor
from .append import Appender
from .thread import DataGetter, DataMapper
from .options import OptionModel

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

    def start(self, accessor: Accessor, appenders: List[Appender], model: OptionModel):
        self.logger_.info("Crawling scheduler running ... ")
        self.running_ = True
        start_time = time.time()

        end_flag = False
        getter = DataGetter(accessor, self.queue_, end_flag, model)
        mapper = DataMapper(appenders, self.queue_, end_flag, model)
        getter.start()
        mapper.start()

        while self.running_:
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.sleep_time_:
                start_time = time.time()
                getter.start()
                mapper.start()
            else:
                self.logger_.info("Crawling condition is health. to continue crawling ... ")
                time.sleep(self.check_time_)
            time.sleep(self.interval_time_)

        getter.kill()
        getter.join()
        mapper.join()

        self.logger_.info("Crawling scheduler shutdown")

    def stop(self) -> object:
        self.running_ = False

class FullTimeScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.running_ = False

    def start(self):
        return None

    def stop(self) -> object:
        self.running_ = False