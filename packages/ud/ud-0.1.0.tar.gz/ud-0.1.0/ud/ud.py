from urllib.request import (urlopen, Request)
from urllib.parse import (quote, urlunparse, urlencode)
from urllib.error import HTTPError
from urllib.error import URLError
import json
import re
import requests
from lxml import html

# YAY COPY AND PASTE CODE 4 LIFE

def define(msg):
    # http://api.urbandictionary.com/v0/define?term=lmao
    scheme = "http"
    netloc = "api.urbandictionary.com"
    path = "/v0/define"
    params = ""

    query = urlencode([
        ("term", "%s" % msg)])
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

    try:
        return_def = resultFINALLY["list"][0]["definition"]

        return_example = resultFINALLY["list"][0]["example"]

    except IndexError:
        return "No results found."

    UDDEF = {"title": msg, "definition": return_def, "example": return_example}

    return(UDDEF)

def random():
    # http://www.urbandictionary.com/random.php
    random_page = requests.get("http://urbandictionary.com/random.php")
    get_stuff = html.fromstring(random_page.content)
    word = get_stuff.xpath('//a[@class="word"]/text()')[0]
    return define(word)

