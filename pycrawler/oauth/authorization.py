#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import urllib.parse
import webbrowser
import requests
from requests_oauthlib import OAuth1, OAuth2

class OAuthModel(object):

    def __init__(self, api: str):
        self.logger_ = logging.getLogger(__name__)
        self.organization_ = api.split(".")[0]
        self.access_token_ = None

    def auth(self, api_key: str, api_secret: str) -> object:
        self.api_key_, self.api_secret_ = api_key, api_secret
        with open(os.path.join(os.path.dirname(__file__), "../../conf/" + self.organization_ + ".conf"), "r") as f:
            lines = f.readlines()
        configure = {line.split("=")[0]: line.split("=")[1].strip() for line in lines}
        self.logger_.info(f"Success loading the authentication of {self.organization_} configure.")
        request_url, authorize_url, access_token_url = configure["REQUEST_URL"], configure["AUTHORIZE_URL"], configure["ACCESS_TOKEN_URL"]
        callback_uri = configure["CALLBUCK_URI"]
        auth = OAuth1(self.api_key_, self.api_secret_, callback_uri=callback_uri)
        response = requests.post(request_url, auth=auth)
        request_token = dict(urllib.parse.parse_qsl(response.text))
        self.logger_.info(f"Success get to request token on this crawling application by {request_url}")

        webbrowser.open(f"{authorize_url}?oauth_token={request_token['oauth_token']}&perms=delete")
        oauth_verifier = input("Please input PIN code : ")
        auth = OAuth1(
            self.api_key_,
            self.api_secret_,
            request_token["oauth_token"],
            request_token["oauth_token_secret"],
            verifier=oauth_verifier
        )
        response = requests.post(access_token_url, auth=auth)
        self.access_token_ = dict(urllib.parse.parse_qsl(response.text))
        self.logger_.info(f"Success get to access token on this crawling application by {access_token_url}")
        return self