#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycrawler.interface import Crawler
from pycrawler.core.manage import TimeScheduler
from pycrawler.core.append import FileAppender, PostgreSQLAppender

if __name__ == "__main__":
    with open("./tests/api.conf", "r") as f:
        lines = f.readlines()
    api_config = {line.split("=")[0]: line.split("=")[1] for line in lines}
    api = "flickr.photos.search"

    flickrCrawler = Crawler(api=api, scheduler=TimeScheduler(), appenders=[FileAppender(), PostgreSQLAppender()])
    flickrCrawler.auth(api_config["CONSUMER_KEY"], api_config["CONSUMER_SECRET"])
    flickrCrawler.run()
