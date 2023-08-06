import sys

from urllib.request import urlopen
from urllib.parse import (urlunparse, urlencode)
from urllib.error import HTTPError
from urllib.error import URLError
from generated_dict import *
import json

API_KEY = None

__author__ = "dizaztor"


def api(api_key):
    global API_KEY
    API_KEY = api_key


def detect(msg):
    scheme = "https"
    netloc = "translation.googleapis.com"
    path = "/language/translate/v2/detect"
    params = ""
    TEXT = "%s" % msg

    if API_KEY is None:
        return("API key not specified.")
        sys.exit(0)
    else:
        pass

    query = urlencode([
        ("q", TEXT),
        ("key", API_KEY)])
    fragment = ""
    FINALLY = urlunparse((scheme, netloc, path, params, query, fragment))

    try:
        FINALLY1 = urlopen(FINALLY)
    except HTTPError as e:
            print("HTTP Error:", e.code)

    except URLError as e:
            print("URL Error:", e.reason)

    try:
        resultFINALLY = json.loads(FINALLY1.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")

    return_lang = resultFINALLY["data"]["detections"][0][0]["language"]

    return(codes[return_lang])
