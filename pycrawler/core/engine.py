#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet import defer, task


class ExecutionEngine(object):

    def __init__(self, crawler, closed_callback=None):
        self.crawler = crawler
        self.running = False
        self._closed_callback = closed_callback

    def start(self):
        """Start the execution engine"""
        self.running = True

    def stop(self):
        """Stop the execution engine gracefully"""
        assert(self.running, "Engine not running")
        self.running = False

    def crawl(self):
        """Spider Event"""

    def schedule(self):
        """Schedule Event"""

    def download(self):
        """Download Event"""
