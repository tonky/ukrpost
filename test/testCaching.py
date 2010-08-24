#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sqlite3
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


class TestCaching(unittest.TestCase):
    def setUp(self):
        self.p = Process(target=run_once)
        self.p.start()
        time.sleep(0.1)

        self.conn = sqlite3.connect(os.path.join(os.getcwd(), '/tmp/test.sqlite3'))
        self.cursor = self.conn.cursor()

        self.cursor.execute('drop table if exists address')
        self.cursor.execute('drop table if exists track')
        self.cursor.execute('create table address (postcode integer, address text)')
        self.cursor.execute('create table track (number integer, ifo text)')

        self.conn.commit()

        self.post_49069 = {"address_full": "", "phone": "12345", "street": "",
                "place": "", "coordinates": "", "zipcode": 49069}


    """
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
        self.assertEqual(filial['place'], u"Дніпропетровськ")
        self.assertEqual(filial['coordinates'], {u"lat": 48.4451160, u"lng": 35.0259140})

    """

    def test_cached_index(self):
        self.cursor.execute("insert into address values (?, ?)",
                (49069, json.dumps(self.post_49069)))

        self.conn.commit()

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        end = time.time()

        filial = json.loads(html)

        self.assertTrue((end - start) < 0.3)
        self.assertEqual(filial['phone'], "12345")
        self.assertEqual(filial['zipcode'], 49069)

    def test_noncached_index(self):
        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        end = time.time()

        filial = json.loads(html)

        self.assertTrue((end - start) > 0.4)


    def tearDown(self):
        self.cursor.close()


if __name__ == '__main__':
    unittest.main()
