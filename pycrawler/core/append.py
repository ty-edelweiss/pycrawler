#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import threading
import psycopg2

from typing import List, Dict, Any

class Appender(object):

    def __init__(self, *args, **kwargs):
        """
        data appender multi format -> default format [ConsoleAppender].
        """

    def append(self, *args, **kwargs) -> None:
        """
        appending process by multi format
        and this method is overrided absolutely.
        """

class ConsoleAppender(Appender):

    def __init__(self, options: Dict[str, Any] = None):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.name_ = "console"
        self.options_ = options

    def setOptions(self, options: Dict[str, Any]):
        self.options_ = options
        return self

    def append(self, data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            print(data, flush=True)

class FileAppender(Appender):

    def __init__(self, options: Dict[str, Any] = None):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.name_ = "file"
        self.options_ = options

    def setOptions(self, options: Dict[str, Any]):
        self.options_ = options
        return self

    def append(self, data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            if os.path.isfile(self.options_["file"]):
                headers = ", ".join(self.options_["columns"])
                with open(self.options_["file"], "w") as f:
                    f.write(headers)
            try:
                with open(self.options_["flie"], "a") as f:
                    f.write(",".join(data))
                self.logger_.info("Success write to " + self.options_["path"] + " with csv")
            except IndexError as err:
                self.logger_.error(err)
            except IOError as err:
                self.logger_.error(err)
            return None

class PostgreSQLAppender(Appender):

    def __init__(self, options: Dict[str, Any] = None):
        super().__init__()
        self.lock_ = threading.Lock()
        self.logger_ = logging.getLogger(__name__)
        self.name_ = "database.postgresql"
        self.connection_ = psycopg2.connect(options["database"]) if options is not None else None
        self.cursor_ = self.connection_.cursor() if options is not None else None
        self.options_ = options

    def setOptions(self, options: Dict[str, Any]):
        self.options_ = options
        self.connection_ = psycopg2.connect(**self.options_["database"])
        self.cursor_ = self.connection_.cursor()
        return self

    def append(self, data: List[Dict[str, Any]]) -> None:
        with self.lock_:
            table_values = ", ".join(["%s" for _ in range(len(self.options_["columns"]))])
            try:
                table_columns = ", ".join(self.options_["columns"])
                self.cursor_.execute(f"INSERT {self.options_['table']} ({table_columns}) VALUES ({table_values})", data)
                self.connection_.commit()
                self.logger_.info("Success insert to postgresql database")
            except psycopg2.ProgrammingError as err:
                self.connection_.rollback()
                self.logger_.error(err)
            return None