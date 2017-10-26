#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Scheduler(object):

    def __init__(self):
        self.queue = []

    def _push(self, request):
        self.queue.append(request)

    def _pop(self):
        return self.queue.pop()
