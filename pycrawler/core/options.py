#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from xml.dom import minidom
from xml.etree import ElementTree
from typing import List, Dict, Any
from ..oauth.authorization import OAuth
from ..util.utils import xmlToTreeDict, treeDictSearch, formatDict

class OptionModel(object):

    def __init__(self, *args, **kwargs):
        """
        application option registering model.
        """

    def register(self, *args, **kwargs):
        """
        register options to model.
        """

class AppOptionModel(OptionModel, OAuth):

    def __init__(self, api: str):
        super(OptionModel, self).__init__(api)
        self.logger_ = logging.getLogger(__name__)
        self.api_ = api
        self.params_ = []
        self.session_ = None

    def validateConfigure(self, userConfig: Dict[str, Any], currentConfig: ElementTree) -> None:
        return None

    def __contentsTree(self, top: ElementTree, contentset: List[Dict[str, Any]]) -> None:
        formattedContents = formatDict(dict(), contentset[0])
        for contents in contentset[1:]:
            formattedContents = formatDict(formattedContents, contents)
        for key, value in formattedContents.items():
            node = ElementTree.SubElement(top, "node")
            node.set("name", key)
            node.set("column", key)
            node.set("type", str(value["type"]))
            example = str(value["value"]).strip()
            node.set("example", example if len(example) < 20 else example[:20] + "...")
            node.set("target", "")
            node.text = "NULL"
        return None

    def oauth(self, api_key: str, api_secret: str) -> object:
        self.session_ = super().auth(api_key, api_secret)
        if len(self.params_) > 0: self.options_["oauth"] = self.session_
        return self

    def create(self, user_config: Dict[str, Any], api_contentset: List[Dict[str, Any]]) -> object:
        root = ElementTree.Element("application")
        api = ElementTree.SubElement(root, "api")
        api.set("name", self.api_)
        params = ElementTree.SubElement(api, "parameters")
        for key, value in user_config.items():
            node = ElementTree.SubElement(params, "node")
            node.set("name", key)
            node.text = value
        oauth = ElementTree.SubElement(api, "oauth")
        oauth.set("key", self.api_key_ if self.api_key_ is not None else "")
        oauth.set("secret", self.api_secret_ if self.api_secret_ is not None else "")
        if self.session_ is not None:
            token = ElementTree.SubElement(oauth, "token")
            token.text = self.access_token_
            secret = ElementTree.SubElement(oauth, "secret")
            secret.text = self.access_token_secret_
        file = ElementTree.SubElement(root, "file")
        file.set("path", "./tmp/")
        file.text = self.organization_ + ".csv"
        database = ElementTree.SubElement(root, "database")
        database.set("host", "")
        database.set("port", "")
        database.set("username", "")
        database.set("password", "")
        database.text = "postgres"
        table = ElementTree.SubElement(database, "table")
        table.set("created", "")
        table.text = self.organization_
        contents = ElementTree.SubElement(root, "contents")
        contents.set("all", "")
        self.__contentsTree(contents, api_contentset)
        if not os.path.isdir("./resources"): os.makedirs("./resources")
        xml_string = minidom.parseString(ElementTree.tostring(root)).toprettyxml(indent="  ")
        with open("./resources/application.xml", "w", encoding="utf-8") as f:
            f.write(xml_string)
        return self

    def defaultLoad(self, user_config: Dict[str, Any]) -> object:
        tree = ElementTree.parse(os.path.join(os.path.dirname(__file__), "../../conf/" + self.organization_ + ".xml"))
        root_config = xmlToTreeDict(tree.getroot())
        self.options_ = {
            "url": root_config["organization"]["@url"],
            "status": root_config["organization"]["@status"],
            "statuscode": root_config["organization"]["@statuscode"],
            "parameters": dict()
        }
        api_name = self.api_.split(".")
        if len(api_name) == 2:
            api_method = treeDictSearch(root_config, "api" + "#" + api_name[1])
            self.options_["contents"] = treeDictSearch(api_method, "@contents")
        elif len(api_name) == 3:
            api_method = treeDictSearch(root_config, "method" + "#" + api_name[1])
            api_method = treeDictSearch(api_method, "api" + "#" + api_name[2])
            self.options_["contents"] = treeDictSearch(api_method, "@contents")
        else:
            raise AssertionError("Api method is invalid. please, selecting dot hierarchy api name.")
        for node in [value for key, value in api_method.items() if "node" in key]:
            if node["@name"] in user_config:
                self.options_["parameters"][node["@name"]] = user_config[node["@name"]]
            elif node["@required"] == "api":
                self.options_["parameters"][node["@name"]] = self.api_
            elif node["@required"] == "format":
                self.options_["parameters"][node["@name"]] = node["@protocol"]
            elif node["@required"] == "patch":
                self.options_["parameters"][node["@name"]] = node["@protocol"]
            else:
                pass
            self.params_.append(node)
        self.options_["oauth"] = self.session_ if self.session_ is not None else None
        return self

    def load(self, user_config: Dict[str, Any]) -> object:
        tree = ElementTree.parse(os.path.join(os.path.dirname(__file__), "../../conf/" + self.organization_ + ".xml"))
        root_config = xmlToTreeDict(tree.getroot())
        self.options_ = {
            "url": root_config["organization"]["@url"],
            "status": root_config["organization"]["@status"],
            "statuscode": root_config["organization"]["@statuscode"],
            "parameters": dict()
        }
        api_name = self.api_.split(".")
        if len(api_name) == 2:
            api_method = treeDictSearch(root_config, "api" + "#" + api_name[1])
            self.options_["contents"] = treeDictSearch(api_method, "@contents")
        elif len(api_name) == 3:
            api_method = treeDictSearch(root_config, "method" + "#" + api_name[1])
            api_method = treeDictSearch(api_method, "api" + "#" + api_name[2])
            self.options_["contents"] = treeDictSearch(api_method, "@contents")
        app_tree = ElementTree.parse("./resources/application.xml")
        app_config = xmlToTreeDict(app_tree.getroot())
        app_params = treeDictSearch(app_config, "parameters")
        self.validateConfigure(user_config, app_config)
        for node in [value for key, value in api_method.items() if "node" in key]:
            if node["@name"] in user_config:
                self.options_["parameters"][node["@name"]] = user_config[node["@name"]]
            elif node["@name"] in app_params:
                self.options_["parameters"][node["@name"]] = app_params[node["@name"]]
            elif node["@required"] == "api":
                self.options_["parameters"][node["@name"]] = self.api_
            elif node["@required"] == "format":
                self.options_["parameters"][node["@name"]] = node["@protocol"]
            elif node["@required"] == "patch":
                self.options_["parameters"][node["@name"]] = node["@protocol"]
            else:
                pass
            self.params_.append(node)
        oauth_params = treeDictSearch(app_config, "oauth")
        self.session_ = self.createSession(
            oauth_params["@key"],
            oauth_params["@secret"],
            oauth_params["token"]["text"],
            oauth_params["secret"]["text"]
        )
        self.options_["oauth"] = self.session_
        file_params = treeDictSearch(app_config, "file")
        self.options_["file"] = file_params["@path"] + file_params["text"]
        print(self.options_["file"])
        db_params = treeDictSearch(app_config, "database")
        print(db_params)
        self.options_["database"] = { "dbname": db_params["text"], "host": db_params["@host"], "port": db_params["@port"], "user": db_params["@username"], "password": db_params["@password"]}
        self.options_["columns"] = [value["@column"] for key, value in app_config["application"]["contents"].items() if "node" in key and value["@target"]]
        self.options_["names"] = [value["@name"] for key, value in app_config["application"]["contents"].items() if "node" in key and value["@target"]]
        return self
