#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import queue
import threading
from typing import List, Tuple, Any

from .access import ApiAccessor, FileAccessor
from .config import checkAppArguments, checkApiArguments
from ..oauth.authorization import OAuth

class DataGetter(threading.Thread):

    def __init__(self, queue: Queue, flagment: bool, app_options: Dict[str, Any], **kwrds):
        super(Flickr).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = queue
        self.flagment_ = flagment
        self.running_ = False

    def kill(self):
        self.running_ = False
        return self

    def run(self, api_options: Dict[str, Any], **kwrds) -> None:
        self.running_ = True

        accessor = ApiAccessor(api_options)
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

    def __init__(self, queue: Queue, flagment: bool, app_options: Dict[str, Any], **kwrds):
        super(DataMapper).__init__()
        self.logger_ = logging.getLogger(__name__)
        self.queue_ = queue
        self.flagment_ = flagment
        self.running_ = False

    def kill(self) -> object:
        self.running_ = False
        return self

    def run(self, api_options: Dict[str, Any], **kwrds) -> None:
        self.running_ = True

        accessors = [PostgreSQLAccessor(data_options), FileAccessor(data_options)]
        while self.running_:
            self.logger_.info("Data mapper process running ... ")
            if self.flagment_ and self.queue_.empty():
                break
            else:
                datum = self.queue_.get()
                for accessor in accesors:
                    accessor.insert(datum)

        self.logger_.info("Data mapper process shutdown")
