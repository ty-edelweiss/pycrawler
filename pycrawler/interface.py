#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging
from typing import List, Dict, Any

from .core.manage import Scheduler, TimeScheduler
from .core.access import Accessor, ApiAccessor
from .core.append import Appender, ConsoleAppender
from .core.options import OptionModel, AppOptionModel

class Crawler(object):

    def __init__(self,
                 scheduler: Scheduler = TimeScheduler(),
                 accessor: Accessor = ApiAccessor(),
                 appenders: List[Appender] = [ConsoleAppender()]):
        self.logger_ = logging.getLogger(__name__)
        self.scheduler_ = scheduler
        self.accessor_ = accessor
        self.appenders_ = appenders

    def register(self,
                 api: str,
                 api_key: str = None,
                 api_secret: str = None,
                 api_params: Dict[str, Any] = None) -> object:
        self.model_ = AppOptionModel(api)
        if not os.path.isfile("./resources/application.xml"):
            self.model_.oauth(api_key, api_secret).defaultLoad(api_params)
            contents = ApiAccessor(self.model_.options_).get()
            self.model_.create(api_params, contents)
            self.logger_.warning("Application configure is create defaulted. please, setting configure, and restart application")
            sys.exit(1)
        else:
            self.model_.load(api_params)
            if self.model_.session_ is None: self.model_.oauth(api_key, api_secret)
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
        self.scheduler_.start(self.accessor_, self.appenders_, self.model_)

class Explorer(object):

    def __init__(self, accessor: Accessor = ApiAccessor()):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.accesor_ = accessor

    def execute(self, api_params: Dict[str, Any], **kwrds):
        pass
        return None