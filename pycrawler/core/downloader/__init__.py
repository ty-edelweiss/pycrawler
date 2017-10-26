#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet import defer, task


class Downloader(object):

    def __init__(self):
        self.active = set()

    def fetch(self, request):
        self.active.add(request)
