#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys, os
sys.path.append(os.getcwd()) 
from post import delivery_info, filial_info
from wsgi import run_once, run
from multiprocessing import Process
import urllib, urllib2
import time

try:
    import json
except ImportError:
    import simplejson as json


class TestAsServer(unittest.TestCase):
    def setUp(self):
        self.p = Process(target=run_once)
        self.p.start()
        time.sleep(0.1)

    def test_search_track(self):
        url = 'http://localhost:8000/track/RB193328726HK'
        f = urllib.urlopen(url)
        info = f.info()
        html = f.read().strip()
        f.close()

        self.assertEqual("application/json", info.gettype())

        filial = json.loads(html)

        self.assertEqual(filial['zipcode'], 49069)
        self.assertEqual(filial['updated'], "04.08.2010")
        self.assertEqual(filial['status_full'], u"Відправлення за номером RB193328726HK \
передано 04.08.2010 в об'єкт поштового зв'язку ДНІПРОПЕТРОВСЬК 69 з \
індексом 49069, на даний час не вручене.")
        self.assertEqual(filial['address_full'], u"Відділення поштового зв'язку № 69 м. \
Дніпропетровськ Поштамту - ЦПЗ № 1 Дніпропетровської дирекції \
Українського державного підприємства поштового зв'язку \
\"Укрпошта\"")
        self.assertEqual(filial['street'], u"вул. Г. Сталінграда, 8")
        self.assertEqual(filial['phone'], "749-69-92")

    def test_search_index(self):
        url = 'http://localhost:8000/index/49069'
        f = urllib.urlopen(url)
        info = f.info()
        html = f.read().strip()
        f.close()

        self.assertEqual("application/json", info.gettype())

        filial = json.loads(html)

        self.assertEqual(filial['address_full'], u"Відділення поштового зв'язку № 69 м. \
Дніпропетровськ Поштамту - ЦПЗ № 1 Дніпропетровської дирекції \
Українського державного підприємства поштового зв'язку \
\"Укрпошта\"")
        self.assertEqual(filial['street'], u"вул. Г. Сталінграда, 8")
        self.assertEqual(filial['phone'], "749-69-92")

    def test_help(self):
        url = 'http://localhost:8000/help.html'
        f = urllib.urlopen(url)
        info = f.info()
        html = f.read().strip()
        f.close()

        self.assertEqual("<html>/index/49069 for post office info<br/><br/>\
\n/track/xxxxxxxxxxxxxxxx for full tracking info\n</html>", html)

        self.assertEqual("text/html", info.gettype())

    def test_static_text(self):
        url = 'http://localhost:8000/test/unicode.txt'
        f = urllib.urlopen(url)
        html = f.read()
        info = f.info()
        f.close()

        self.assertEqual("привет!", html)
        self.assertEqual("text/plain", info.gettype())

    def test_static_css(self):
        url = 'http://localhost:8000/test/test.css'
        f = urllib.urlopen(url)
        html = f.read()
        info = f.info()
        f.close()

        self.assertEqual("text/css", info.gettype())
        self.assertEqual(html, "{ font: 1px; }")


    def test_static_js(self):
        url = 'http://localhost:8000/test/test.js'
        f = urllib.urlopen(url)
        html = f.read()
        info = f.info()
        f.close()

        self.assertEqual("application/javascript", info.gettype())
        js = json.loads(html)
        self.assertEqual(js['hi'], "me")

    def test_static_miss(self):
        url = 'http://localhost:8000/bazinga'
        f = urllib.urlopen(url)
        html = f.read()
        f.close()

        self.assertEqual("Not found", html)


if __name__ == '__main__':
    unittest.main()
