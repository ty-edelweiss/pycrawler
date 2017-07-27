#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import threading
import requests
from typing import List, Dict, Any

class Accessor(object):

    def __init__(self, *args, **kwargs):
        """
        data accessor to api by target url.
        """

    def get(self, *args, **kwargs) -> Any:
        """
        accessing process by target url
        and this method is overrided absolutely.
        """

class ApiAccessor(Accessor):

    def __init__(self, options: Dict[str, Any] = None):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.status_ = options["statuscode"] if options is not None else None
        self.options_ = options

    def setOptions(self, options: Dict[str, Any]):
        self.options_ = options
        self.status_ = self.options_["statuscode"]
        return self

    def next(self) -> bool:
        return self.status_ == "ok"

    def get(self, payload: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with self.lock_:
            if self.options_ is None: AssertionError("Access parameter is not defined.")
            if payload is not None: self.options_["parameters"].update(payload)
            try:
                response = requests.get(self.options_["url"], params=self.options_["parameters"], auth=self.options_["oauth"])
                self.logger_.info("Success http access to " + self.options_["url"])
                obj = json.loads(response.text)
                status_code = obj[self.options_["status"]]
                if status_code == self.options_["statuscode"]:
                    self.status_ = obj[self.options_["status"]]
                    for key in self.options_["contents"].split("."):
                        obj = obj[key]
                    return obj if type(obj).__name__ == "list" else [obj]
                else:
                    self.logger_.error(f"Request parameters is invalid. because return status code is {status_code}")
                    return []
            except requests.exceptions.ConnectionError as err:
                self.logger_.error(err)
                return None
            except requests.exceptions.HTTPError as err:
                self.logger_.error(err)
                return None
            except requests.exceptions.Timeout as err:
                self.logger_.error(err)
                return None

