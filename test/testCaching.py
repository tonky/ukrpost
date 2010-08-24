#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sqlite3
import sys, os
sys.path.append(os.getcwd()) 
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

        self.conn = sqlite3.connect(os.path.join(os.getcwd(), 'ukrpost.sqlite3'))
        self.cursor = self.conn.cursor()

        self.cursor.execute('drop table if exists address')
        self.cursor.execute('drop table if exists track')
        self.conn.commit()

        self.cursor.execute('create table address (postcode integer, address blob)')
        self.cursor.execute('create table track (number integer, info blob)')

        self.conn.commit()

        self.post_49069 = {"address_full": "", "phone": "12345", "street": "",
                "place": "", "coordinates": ""}

    def test_noncached_index(self):
        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) > 0.4)

    def test_cached_index(self):
        self.cursor.execute("insert into address values (?, ?)",
                (49069, json.dumps(self.post_49069)))

        self.conn.commit()

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) < 0.1)

        filial = json.loads(html)

        self.assertEqual(filial['phone'], "12345")

    def tearDown(self):
        self.cursor.close()


if __name__ == '__main__':
    unittest.main()
