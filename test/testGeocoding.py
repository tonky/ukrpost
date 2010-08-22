#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys, os
sys.path.append(os.getcwd()) 
from post import delivery_info, filial_info
from geocode import geocode
import urllib, urllib2
import time

try:
    import json
except ImportError:
    import simplejson as json


class TestGeocoding(unittest.TestCase):
    def test_geo(self):
        self.assertEqual(geocode(u"Дніпропетровськ"),
            {u'lat': 48.45, 
            u'lng': 34.9833333})

        self.assertEqual(geocode(u"Царичанка"),
            {u'lat': 48.9461111, 
            u'lng': 34.4780556})

        self.assertEqual(geocode(u"ичанка"), {})

        with open(os.path.join(os.getcwd(), 'test/html/49069.html'), 'r') as f:
            html = f.read()

        parsed = filial_info(html, u"Дніпропетровськ")

        self.assertEqual(geocode(parsed['place'], parsed['street']),
            {u'lat': 48.4451160, 
            u'lng': 35.0259140})


if __name__ == '__main__':
     unittest.main()

