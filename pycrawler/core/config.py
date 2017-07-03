#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from xml.etree import ElementTree

from typing import List, Any

APP = None
API = None

def registerAppArguments(udc: Dict[str, Any], **kwrds) -> None:
    if udc is None: udc = kwrds
    return None

def registerApiArguments(udc: Dict[str, Any], **kwrds) -> None:
    if udc is None: udc = kwrds
    tree = ElementTree.parse(os.path.join(__file__, "../conf/api.xml"))
    root = tree.getroot()
    method = filter(lambda child: child.name == udc.method, root)
    API = {child.name: udc[child.name] if child.name in udc else child.value for child in method}
    return None
