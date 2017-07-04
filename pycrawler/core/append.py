#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import threading
import psycopg2

from typing import List, Dict, Any

class Appender(object):

    def __init__(self, *args, **kwrds):
        """
        data appender multi format -> default format [ConsoleAppender].
        """

    def append(self, *args, **kwrds) -> None:
        """
        appending process by multi format
        and this method is overrided absolutely.
        """

class ConsoleAppender(Appender):

    def __init__(self):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)

    def append(self, data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            print(data)

class FileAppender(Appender):

    def __init__(self, target: str):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.self.file_path__ = target

    def append(self, column_names: List[str], data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            if os.path.isfile(self.file_path_):
                headers = ", ".join(column_names)
                with open(self.file_path_, "w") as f:
                    f.write(headers)
            try:
                with open(self.file_path_, "a") as f:
                    f.write(",".join(data))
                self.logger_.info("Success write to " + self.file_path_ + " with csv")
            except IndexError as err:
                self.logger_.error(err)
            except IOError as err:
                self.logger_.error(err)
            return None

class PostgreSQLAppender(Appender):

    def __init__(self, connection: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.conn_ = connection
        self.cur_ = cursor

    def append(self, table_name: str, column_names: List[str], data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            table_columns = ", ".join(["%s" for _ in range(column_names)])
            try:
                self.cur_.execute(f"INSERT {table_name} ({table_columns}) VALUES ({column_names})", data)
                self.conn_.commit()
                self.logger_.info("Success insert to postgresql database")
            except psycopg2.ProgrammingError as err:
                self.logger_.error(err)
            return None

