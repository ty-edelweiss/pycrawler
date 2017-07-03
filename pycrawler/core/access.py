#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import threading
import requests
import psycopg2
from typing import List, Any

class ApiAccessor(object):

    def __init__(self, ):
        self.lock_ = threading.Lock()
        self.logger_ = logging.logger(__name__)
        self.url_ = "http://api.flickr.com/services/rest"
        self.status_ = "ok"

    def next(self) -> bool:
        return self.status_ == "ok"

    def get(self, payload: Dict[str, Any], **kwrds) -> List[Dict[str, Any]]:
        with self.lock_:
            if payload is None: payload = kwrds
            try:
                response = requests.get(sel.url_, params=payload)
                self.logger_.info("Success http access to " + url)
                obj =  json.loads(response.text)
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

class PostgreSQLAccessor(object):

    def __init__(self, connection: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
        self.lock_ = threading.Lock()
        self.logger_ = logging.logger(__name__)
        self.conn_ = connection
        self.cur_ = cursor

    def set(self, table_name: str, column_names: List[str], data: Dict[str, Any]) -> None:
        with self.lock_:
            column_names = ", ".join(["%s" for _ in range(columns)])
            try:
                self.cur_.execute(f"INSERT {table_name} VALUES ({column_names})", data)
                self.conn_.commit()
                self.logger_.info("Success insert to postgresql database")
            except psycopg2.ProgrammingError as err:
                self.logger_.error(err)
            return None

class FileAccessor(object):

    def __init__(self, max_bytes: int = 1000, max_backups: int = 3):
        self.lock_ = threading.Lock()
        self.logger_ = logging.logger(__name__)
        self.max_bytes_ = max_bytes_
        self.max_buckups_ = max_buckups_

    def set(self, file_path: str, column_names: List[str], data: Dict[str, Any]) -> None:
        with self.lock_:
            if os.path.isfile(file_path):
                column_names = ", ".join(["%s" for _ in range(columns)])
                with open(file_path, "w") as f:
                    f.write(column_names)
            try:
                with open(file_path, "a") as f:
                    f.write(",".join(data))
                self.logger_.info("Success write to " + path + " with csv")
            except IndexError as err:
                self.logger_.error(err)
            except IOError as err:
                self.logger_.error(err)
            return None

