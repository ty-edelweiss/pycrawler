#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from xml.etree import ElementTree
from typing import List, Dict, Any
from ..oauth.authorization import OAuthModel

class OptionModel(object):

    def __init__(self, *args, **kwrds):
        """
        application option registering model.
        """

    def register(self, *args, **kwrds):
        """
        register options to model.
        """

class DataOptionModel(OptionModel):

    def __init__(self):
        super(OptionModel, self).__init__()
        self.logger_ = logging.getLogger(__name__)

    def load(self, userDefineConfig: Dict[str, Any]):
        with open(os.path.join(os.path.dirname(__file__), "../../conf/default.conf")) as f:
            lines = f.readlines()
        self.options_ = {line.split("=")[0]: line.split("=")[1].strip() for line in lines}
        if userDefineConfig is not None:
            for key, value in userDefineConfig.items():
                self.options_[key] = value
        return self

class ApiOptionModel(OptionModel, OAuthModel):

    def __init__(self, api: str):
        super().__init__(api)
        self.logger_ = logging.getLogger(__name__)
        self.method_ = api.split(".")[-1]

    def load(self, userDefineConfig: Dict[str, Any]):
        tree = ElementTree.parse(os.path.join(os.path.dirname(__file__), "../conf/" + self.organization_ + ".xml"))
        root = tree.getroot()
        method = filter(lambda child: child.name == self.method_, root)
        self.options_ = {child.name: child.value for child in method}
        if userDefineConfig is not None:
            for key, value in userDefineConfig.items():
                self.options_[key] = value
        return self
