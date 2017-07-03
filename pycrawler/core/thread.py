#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import queue
import threading
from typing import List, Dict, Any

from .access import Accessor
from .append import Appender

class DataGetter(threading.Thread):

    def __init__(self, cache: queue.Queue, flagment: bool, app_options: Dict[str, Any], **kwrds):
        super(DataGetter).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = cache
        self.flagment_ = flagment
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self, accessor: Accessor) -> None:
        self.running_ = True

        while self.running_:
            self.logger_.info("Data getter process running ... ")
            if accessor.next():
                datum = accessor.get()
                self.queue_.push(datum)
            else:
                self.flagment_ = True
                break

        self.logger_.info("Data getter process shutdown")

class DataMapper(threading.Thread):

    def __init__(self, cache: queue.Queue, flagment: bool, app_options: Dict[str, Any], **kwrds):
        super(DataMapper).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = cache
        self.flagment_ = flagment
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self, appenders: List[Appender]) -> None:
        self.running_ = True

        while self.running_:
            self.logger_.info("Data mapper process running ... ")
            if self.flagment_ and self.queue_.empty():
                break
            else:
                datum = self.queue_.get()
                for appender in appenders:
                    appender.set(datum)

        self.logger_.info("Data mapper process shutdown")
