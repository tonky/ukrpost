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

        self.cursor.execute('drop table if exists cache')
        self.conn.commit()

        self.cursor.execute('create table cache (key blob primary key, info blob, expires integer default 0)')

        self.conn.commit()

        self.post_49069 = {"address_full": "", "phone": "12345", "street":
                u"Комсомолська", "place": "", "coordinates": ""}

        self.track = {"address_full": "", "phone": "54321", "street":
                u"Комсомолська", "place": "", "coordinates": "", "zipcode": 49000}

    def test_noncached_track(self):
        start = time.time()

        f = urllib.urlopen('http://localhost:8000/track/RB193328726HK')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) > 0.4)

    def test_cached_expired_track(self):
        self.cursor.execute("insert into cache values (?, ?, ?)",
                ('RB193328726HK', json.dumps(self.track), time.time() - 5))

        self.conn.commit()

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/track/RB193328726HK')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) > 0.4)

        track = json.loads(html)

        self.assertEqual(track['street'], u"вул. Г. Сталінграда, 8")
        self.assertEqual(track['phone'], "749-69-92")
        self.assertEqual(track['place'], u"Дніпропетровськ")
        self.assertEqual(track['coordinates'], {u"lat": 48.4451160, u"lng": 35.0259140})

    def test_cache_track_on_reading(self):
        f = urllib.urlopen('http://localhost:8000/track/RB193328726HK')
        html = f.read().strip()
        f.close()

        self.p = Process(target=run_once)
        self.p.start()
        time.sleep(0.1)

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/track/RB193328726HK')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) < 0.2)

    def test_cached_track(self):
        self.cursor.execute("insert into cache values (?, ?, ?)",
                ('RB193328726HK', json.dumps(self.track), time.time() + 100))

        self.conn.commit()

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/track/RB193328726HK')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) < 0.2)

        track = json.loads(html)

        self.assertEqual(track['phone'], "54321")
        self.assertEqual(track['street'], u"Комсомолська")
        self.assertEqual(track['zipcode'], 49000)

    def test_noncached_index(self):
        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) > 0.4)

    def test_cached_index(self):
        self.cursor.execute("insert into cache values (?, ?, ?)",
                ("49069", json.dumps(self.post_49069), 0))

        self.conn.commit()

        start = time.time()

        f = urllib.urlopen('http://localhost:8000/index/49069')
        html = f.read().strip()
        f.close()

        self.assertTrue((time.time() - start) < 0.2)

        filial = json.loads(html)

        self.assertEqual(filial['phone'], "12345")
        self.assertEqual(filial['street'], u"Комсомолська")

    def tearDown(self):
        self.cursor.close()


if __name__ == '__main__':
    unittest.main()
