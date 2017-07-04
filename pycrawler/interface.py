#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import logging
from typing import List, Dict, Any

from .core.manage import Scheduler, TimeScheduler
from .core.access import Accessor, ApiAccessor
from .core.append import Appender, ConsoleAppender
from .oauth.authorization import OAuth

class Crawler(OAuth):

    def __init__(self, api: str, scheduler: Scheduler = TimeScheduler(), accessor: Accessor = ApiAccessor(), appenders: List[Appender] = [ConsoleAppender]):
        super().__init__(api)
        self.logger_ = logging.getLogger(__name__)
        self.api_ = api
        self.scheduler_ = scheduler
        self.accessor_ = accessor
        self.appenders_ = appenders

    def signalHandler(self, signal, frame) -> None:
        self.logger_.warning("Terminating crawling application.")
        self.shutdown()

    def shutdown(self) -> None:
        self.logger_.warning("Crawling application shutdown ...")
        self.scheduler_.stop()

    def run(self, api_options: Dict[str, Any], **kwrds) -> None:
        self.logger_.info("Crawling application start up ...")
        signal.signal(signal.SIGINT, self.signalHandler)
        self.scheduler_.start(self.accessor_, self.appenders_)

class Explorer(OAuth):

    def __init__(self, api: str):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.api_ = api

    def get(self, api_options: Dict[str, Any], **kwrds):
        pass
        return None