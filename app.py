#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycrawler.interface import Crawler
from pycrawler.core.manage import TimeScheduler
from pycrawler.core.append import FileAppender, PostgreSQLAppender

if __name__ == "__main__":
    with open("./tests/api.conf", "r") as f:
        lines = f.readlines()
    api_config = {line.split("=")[0]: line.split("=")[1].strip() for line in lines}
    api = "flickr.photos.search"

    api_options = {
        "extras": "description, license, date_upload, date_taken, owner_name, url_sq"
    }
    flickrCrawler = Crawler(scheduler=TimeScheduler())
    flickrCrawler.register(api, api_config["CONSUMER_KEY"], api_config["CONSUMER_SECRET"], api_options)
    flickrCrawler.run()
