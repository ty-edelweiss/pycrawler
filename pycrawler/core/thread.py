#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import queue
import threading
from typing import List, Dict, Any

from .access import Accessor
from .append import Appender
from .options import OptionModel

class DataGetter(threading.Thread):

    def __init__(self, cache: queue.Queue, notice: bool, api_model: OptionModel, **kwrds):
        super(DataGetter).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.cache_ = cache
        self.flag_ = notice
        self.options_ = api_model
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self, accessor: Accessor) -> None:
        self.running_ = True

        while self.running_:
            self.logger_.info("Data getter process running ... ")
            if accessor.next():
                data = accessor.get(self.options_)
                self.cache_.push(data)
            else:
                self.flag_ = True
                break

        self.logger_.info("Data getter process shutdown")

class DataMapper(threading.Thread):

    def __init__(self, cache: queue.Queue, notice: bool, app_model: OptionModel, **kwrds):
        super(DataMapper).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.cache_ = cache
        self.flag_ = notice
        self.options_ = app_model
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self, appenders: List[Appender]) -> None:
        self.running_ = True

        while self.running_:
            self.logger_.info("Data mapper process running ... ")
            if self.flag_ and self.cache_.empty():
                break
            else:
                data = self.cache_.get()
                for appender in appenders:
                    appender.append(data, self.options_)

        self.logger_.info("Data mapper process shutdown")
