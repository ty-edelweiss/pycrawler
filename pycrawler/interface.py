#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal
import logging
from typing import List

from .core.manage import Scheduler, TimeScheduler
from .core.append import Appender, ConsoleAppender
from .oauth.authorization import OAuth

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

file_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(__file__, "../logs/crawler.log"),
    maxBytes=1000,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.getLogger().addHandler(stream_handler)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.DEBUG)

class Crawler(OAauth):

    def __init__(self, api: str, scheduler: Scheduler = TimeScheduler(), appenders: List[Appender] = [ConsoleAppender]):
        super().__init__()
        self.logger_ = logging.getLogger(__name__)
        self.api_ = api
        self.scheduler_ = scheduler
        self.appenders_ = appenders

    def signalHandler(self, signal, frame) -> None:
        self.logger_.warning("Terminating crawling application.")
        self.shutdown()

    def shutdown(self) -> None:
        self.logger_.warning("Crawling application shutdown ...")
        self.scheduler_.stop()

    def run(self) -> None:
        self.logger_.info("Crawling application start up ...")
        signal.signal(signal.SIGINT, self.signalHandler)
        self.scheduler_.start(self.appenders_)