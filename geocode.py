#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import re

try:
    import json
except ImportError:
    import simplejson as json


api = 'http://maps.google.com//maps/api/geocode/json?address=%s,україна&sensor=false'

def geocode(place, address=False):
    full_address = ""

    # strip non-alphanumeric chars, replace spaces with "+", or geocoding
    # will fail for places like "старокостянтинів-5"
    place = re.sub('[0-9\-]', "", place)
    place = place.replace(" ", "+")

    if address:
    # add street address, striping commas and replacing whitespace with "+", 
    # if it is present. append to city name when done
        address = re.sub(",", "", address).replace(" ", "+")

        full_address = "%s,%s" % (address, place)

    return _get_latlng(full_address) or _get_latlng(place)

def _get_latlng(location):
    if not location: return {}

    # encode unicode to ascii, for http call
    url = api % location.encode('utf-8')

    f =  urllib.urlopen(url)
    geo = json.loads(f.read())
    f.close()

    if geo['status'] == "ZERO_RESULTS":
        return {}

    return geo['results'][0]['geometry']['location']
