""" Shared objects and methods. """

import requests

from enum import Enum
from fake_headers import Headers


####
## Property types
####

class PropType(Enum):
    FLAT = 0
    HOUSE = 1
    OTHER = 3

    def __str__(self):
        types = ["flat", "house", "other"]
        return types[self.value]

####
## Scraper model class
####

class ScraperModel():
    def __init__(self):
        self._name = ""

        self._url = ""
        self._url_flats = ""
        self._url_houses = ""

        self._min_page_flats = 0
        self._max_page_flats = 0

        self._min_page_houses = 0
        self._max_page_houses = 0

        self._req = requests.session()

    def parse_page(self, job):
        pass

    def of_name(self, target):
        return "%s_%s.csv" % (self._name, str(target))

    def gen_urls(self, target):
        if (target == PropType.FLAT):
            return list_pages(target, self._url_flats,
                              self._min_page_flats, self._max_page_flats)
        elif (target == PropType.HOUSE):
            return list_pages(target, self._url_houses,
                              self._min_page_houses, self._max_page_houses)

####
## Utility methods
####

def make_entry(proptype):
    """Build a new property entry."""

    return {
        "url": None
        , "address": None
        , "loc" : None
        , "price" : None
        , "m2": None
        , "type": str(proptype)
    }

def read_addr(title):
    """Extracting address from a title."""

    addr = None
    if (title is None): return addr

    sp = title.split(" in ")
    if (len(sp)>1):
        addr = sp[1].lower()

    return addr

def gen_headers():
    """Generate random headers."""

    head = Headers().generate()
    head['Accept-Encoding'] = 'gzip, deflate'
    head['Connection'] = 'close'
    head['DNT'] = '1'

    return head

def list_pages(proptype, baseurl, min, max):
    """Building a list of URLs."""
    return [(baseurl % i, proptype) for i in range(min, max+1)]

def read_html(url, req):
    """Send a simple HTTP request."""

    # Sending request
    r = req.get(url, headers=gen_headers())

    if r.status_code == 200:
        return r.text
    else:
        print ("Cannot reach URL: %s\nStatus code: %s" % (url, r.status_code))
        print (r.text)
        exit()
