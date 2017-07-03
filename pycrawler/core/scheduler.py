#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import logging

from .thread import DataGetter, DataMapper

CHECK_TIME = 3600

class Scheduler(object):

    def __init__(self, sleep_time: int = 86400, interval_time: int = 1):
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = Queue()
        self.sleep_time_ = sleep_time
        self.interval_time_ = iterval_time
        self.running_ = False

    def start(self):
        start_time = time.time()
        crawler = DataGetter(self.queue_).run()
        mapper = DataMapper(self.queue_).run()

        self.running_ = True

        while self.running_:
            self.logger_.info("Crawling scheduler running ... ")
            elapsed_time = time.time() - start_time
            if crawler.running_ or mapper.running_:
                time.sleep(interval_time)
            elif elapsed_time >= self.sleep_time_:
                start_time = time.time()
                crawler = DataGetter(self.queue_).run()
                mapper = DataMapper(self.queue_).run()
            else:
                time.sleep(CHECK_TIME)

        self.logger_.info("Crawling scheduler shutdown")


    def stop(self) -> object:
        self.running_ = False
        return self
