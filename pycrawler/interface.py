#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import logging
from typing import List, Dict, Any

from .core.manage import Scheduler, TimeScheduler
from .core.access import Accessor, ApiAccessor
from .core.append import Appender, ConsoleAppender
from .core.options import OptionModel, DataOptionModel, ApiOptionModel

class Crawler(object):

    def __init__(self,
                 scheduler: Scheduler = TimeScheduler(),
                 accessor: Accessor = ApiAccessor(),
                 appenders: List[Appender] = [ConsoleAppender()],
                 data_options: Dict[str, Any] = None):
        self.logger_ = logging.getLogger(__name__)
        self.scheduler_ = scheduler
        self.accessor_ = accessor
        self.appenders_ = appenders
        self.options_ = DataOptionModel().load(data_options)

    def register(self,
                 api: str,
                 api_key: str = None,
                 api_secret: str = None,
                 api_options: Dict[str, Any] = None) -> object:
        self.api_ = ApiOptionModel(api).load(api_options)
        self.api_.auth(api_key, api_secret)
        return self

    def signalHandler(self, signal, frame) -> None:
        self.logger_.warning("Terminating crawling application.")
        self.shutdown()

    def shutdown(self) -> None:
        self.logger_.warning("Crawling application shutdown ...")
        self.scheduler_.stop()

    def run(self) -> None:
        self.logger_.info("Crawling application start up ...")
        ## signal.signal(signal.SIGINT, self.signalHandler)
        self.scheduler_.start(self.accessor_, self.appenders_, app_model=self.options_, api_model=self.api_)

class Explorer(object):

    def __init__(self, name: str):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.name_ = name

    def execute(self, api_options: Dict[str, Any], **kwrds):
        pass
        return None