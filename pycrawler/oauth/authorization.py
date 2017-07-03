#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
import webbrowser
import requests
from requests_oauthlib import OAuth1, OAuth2

class OAuth(object):

    def __init__(self, api: str):
        self.organization_ = api
        self.access_token_ = None

    def auth(self, api_key: str, api_secret: str) -> object
        self.api_key_, self.api_secret_ = api_key, api_secret
        with open(os.path.join(__file__, "../../conf/", self.organization_, ".xml"), "r") as f:
            lines = f.readlines()
        url = {line.split("=")[0]: line.split("=")[1] for line in lines}
        auth = OAuth1(api_key, api_secret, callback_uri=callback_uri)
        response = requests.post(request_url, auth=auth)
        request_token = dict(urllib.parse.parse_qsl(response.text))

        webbrowser.open(f"{authorize_url}?oauth_token={request_token}&perms=delete")
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
        return self