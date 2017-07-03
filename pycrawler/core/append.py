#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import threading
import psycopg2

from typing import List, Dict, Any

class Appender(object):

    def __init__(self):
        """
        data appender multi format -> default format [ConsoleAppender].
        """

    def set(self) -> None:
        """
        appending process by multi format
        and this method is overrided absolutely.
        """

class ConsoleAppender(Appender):

    def __init__(self):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)

    def set(self, data: Dict[str, Any]) -> None:
        with self.lock_:
            print(data)

class FileAppender(Appender):

    def __init__(self, max_bytes: int = 1000, max_backups: int = 3):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.max_bytes_ = max_bytes
        self.max_buckups_ = max_backups

    def set(self, file_path: str, column_names: List[str], data: Dict[str, Any]) -> None:
        with self.lock_:
            if os.path.isfile(file_path):
                headers = ", ".join(column_names)
                with open(file_path, "w") as f:
                    f.write(headers)
            try:
                with open(file_path, "a") as f:
                    f.write(",".join(data))
                self.logger_.info("Success write to " + file_path + " with csv")
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

    def set(self, table_name: str, column_names: List[str], data: Dict[str, Any]) -> None:
        with self.lock_:
            table_columns = ", ".join(["%s" for _ in range(column_names)])
            try:
                self.cur_.execute(f"INSERT {table_name} ({table_columns}) VALUES ({column_names})", data)
                self.conn_.commit()
                self.logger_.info("Success insert to postgresql database")
            except psycopg2.ProgrammingError as err:
                self.logger_.error(err)
            return None

