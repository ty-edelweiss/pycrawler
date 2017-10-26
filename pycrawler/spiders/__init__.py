#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from pycrawler.http import Request


class Spider(object):

    name = None
    endpoint = None
    custom_settings = None

    def __init__(self, name=None, endpoint=None):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        if endpoint is not None:
            self.endpoint = endpoint
        elif not getattr(self, 'end_point', None):
            raise ValueError(f"{type(self).__name__} must have a endpoint")

    def start_requests(self):
        return Request(self.endpoint)

    def parse(self):
        raise NotImplementedError(f"{self.__class__.__name__}.parse callback is not defined")
