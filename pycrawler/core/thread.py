#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import uuid
import queue
import threading
from typing import List, Dict, Any

from .access import Accessor
from .append import Appender
from .options import OptionModel

class DataGetter(threading.Thread):

    def __init__(self, accessor: Accessor, cache: queue.Queue, notice: bool, model: OptionModel):
        super(DataGetter, self).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.accessor_ = accessor
        self.cache_ = cache
        self.flag_ = notice
        self.model_ = model
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self) -> None:
        self.running_ = True
        self.logger_.info("Data getter process running ... ")

        self.accessor_.setOptions(self.model_.options_)

        while self.running_:
            if self.accessor_.next():
                try:
                    uid = uuid.uuid4()
                    data = self.accessor_.get()
                    self.logger_.info(f"Data collecting to pass other thread. data id is {uid}")
                    self.cache_.put((uid, data), block=True, timeout=10)
                except queue.Full as err:
                    self.logger_.warning(err)
            else:
                self.flag_ = True
                break

        self.logger_.info("Data getter process shutdown")

class DataMapper(threading.Thread):

    def __init__(self, appenders: List[Appender], cache: queue.Queue, notice: bool, model: OptionModel):
        super(DataMapper, self).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.appenders_ = appenders
        self.cache_ = cache
        self.flag_ = notice
        self.model_ = model
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self) -> None:
        self.running_ = True
        self.logger_.info("Data mapper process running ... ")

        for appender in self.appenders_:
            appender.setOptions(self.model_.options_)

        while self.running_:
            if self.flag_ and self.cache_.empty():
                break
            else:
                try:
                    uid, data = self.cache_.get(block=True, timeout=10)
                    self.logger_.info(f"Data mapping to get other thread. data id is {uid}")
                    for appender in self.appenders_:
                        appender.append(data)
                except queue.Empty as err:
                    self.logger_.warning(err)

        self.logger_.info("Data mapper process shutdown")
