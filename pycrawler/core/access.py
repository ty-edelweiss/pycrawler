#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import threading
import requests
from typing import List, Dict, Any

class Accessor(object):

    def __init__(self, *args, **kwrds):
        """
        data accessor to api by target url.
        """

    def get(self, *args, **kwrds) -> Any:
        """
        accessing process by target url
        and this method is overrided absolutely.
        """

class ApiAccessor(Accessor):

    def __init__(self):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.status_ = "ok"

    def next(self) -> bool:
        return self.status_ == "ok"

    def get(self, payload: Dict[str, Any], **kwrds) -> List[Dict[str, Any]]:
        with self.lock_:
            if payload is None: payload = kwrds
            try:
                response = requests.get(self.url_, params=payload)
                self.logger_.info("Success http access to " + self.url_)
                obj = json.loads(response.text)
                self.stauts_ = obj.stat
                return obj
            except requests.exceptions.ConnectionError as err:
                self.logger_.error(err)
                return []
            except requests.exceptions.HTTPError as err:
                self.logger_.error(err)
                return []
            except requests.exceptions.Timeout as err:
                self.logger_.error(err)
                return []

