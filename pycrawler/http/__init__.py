#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Request(object):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None, encoding='utf-8', errback=None):
        self._encoding = encoding
        self.method = method
        self._set_url(url)
        self._set_body(body)
        self.callback = callback
        self.errback = errback
        self.headers = headers

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        self._url = url

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        self._body = body
