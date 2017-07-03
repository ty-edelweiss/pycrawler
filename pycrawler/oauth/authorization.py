#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import webbrowser
from requests_oauthlib import OAuth1

request_url = "https://www.flickr.com/services/oauth/request_token"
authorize_url = "https://www.flickr.com/services/oauth/authorize"
access_token_url = "https://www.flickr.com/services/oauth/access_token"
access_url = "https://api.flickr.com/services/rest/"
callback_uri = "oob"

def oauth_requests():
    auth = OAuth1(API_KEY, SECRET_KEY, callback_uri=callback_uri)
    response = requests.post(request_url, auth=auth)
    request_token = dict(urlparse.parse_qsl(response.text))

    webbrowser.open(f"{authorize_url}?oauth_token={request_token}&perms=delete")
    oauth_verifier = input("Please input PIN code:")
    auth = OAuth1(
        API_KEY,
        SECRET_KEY,
        request_token["oauth_token"],
        request_token["oauth_token_secret"],
        verifier=oauth_verifier
    )
    response = requests.post(access_token_url, auth=auth)
    access_token = dict(urlparse.parse_qsl(response.text))
    return access_token
