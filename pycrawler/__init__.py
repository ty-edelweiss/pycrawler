#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers

__version__ = "0.0.0"

__format__ = "%(asctime)s %(levelname)s %(name)s: %(message)s"

__config__ = "./conf/application.conf"

app = None
if os.path.isfile(__config__):
    with open(__config__, "r") as f:
        lines = f.readlines()
    app = {line.split("=")[0]: line.split("=")[1].strip() for line in lines}
else:
    with open(os.path.join(os.path.dirname(__file__), "../conf/default.conf"), "r") as f:
        lines = f.readlines()
    app = {line.split("=")[0]: line.split("=")[1].strip() for line in lines}

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(__format__))

file_handler = logging.handlers.RotatingFileHandler(
    filename=app["LOG_FILE"],
    maxBytes=100000,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(__format__))

logging.getLogger(__name__).addHandler(stream_handler)
logging.getLogger(__name__).addHandler(file_handler)
logging.getLogger(__name__).setLevel(logging.DEBUG)
