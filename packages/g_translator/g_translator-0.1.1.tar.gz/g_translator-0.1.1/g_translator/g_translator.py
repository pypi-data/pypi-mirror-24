from urllib.request import (urlopen, Request)
from urllib.parse import (quote, urlunparse, urlencode)
from urllib.error import HTTPError
from urllib.error import URLError
import html
import json

API_KEYX = None

def gtranslate_auth(token):
    global API_KEYX
    API_KEYX = token

def translate(msg):
    global API_KEYX
    
    if API_KEYX is not None or API_KEYX != "":
        
        scheme = "https"
        netloc = "translation.googleapis.com"
        path = "/language/translate/v2"
        params = ""
        TEXT = "%s" % msg
        query = urlencode([
            ("target", "en"),
            ("q", TEXT),
            ("key", API_KEYX)])

        fragment = ""
        FINALLYX = urlunparse((scheme, netloc, path, params, query, fragment))

        try:
            FINALLY2 = urlopen(FINALLYX)
        except HTTPError as e:
            print("HTTP Error:", e.code)

        except URLError as e:
            print("URL Error:", e.reason)

        try:
            resultFINALLY = json.loads(FINALLY2.read().decode('utf-8'))
        except ValueError:
            print("Value Error: Invalid server response.")

        return_lang = resultFINALLY["data"]["translations"][0]["translatedText"]
        detected_src_lang = resultFINALLY["data"]["translations"][0]["translatedText"]

        eng_return_lang = html.unescape(return_lang)
        return(eng_return_lang)

    else:
        return("API key not specified.")