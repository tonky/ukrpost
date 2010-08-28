#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys, os 
sys.path.append(os.getcwd()) 
from post import parse_tracking_search, parse_filial_info, parse_filial_searchresult

class TestHtmlParsing(unittest.TestCase):
    def test_delivery_working_on(self):
        f = open(os.path.join(os.getcwd(), 'test/html/track_working_on.html'), 'r')
        html = f.read()
        f.close()

        info = parse_tracking_search(html)

        self.assertEqual(info['zipcode'], 49938)
        self.assertEqual(info['updated'], "26.08.2010")

        self.assertEqual(info['status_full'], "Відправлення за номером CJ203841359US знаходиться \
в процесі оброблення. Востаннє воно зареєстроване 26.08.2010 в об’єкті \
поштового зв’язку Дніпропетровськ ЗВОП Обмін область роб з індексом 49938.")

    def test_delivery(self):
        f = open(os.path.join(os.getcwd(), 'test/html/barcode.html'), 'r')
        html = f.read()
        f.close()

        info = parse_tracking_search(html)

        self.assertEqual({'zipcode': 49069, 'updated': '04.08.2010', 
            'status_full': "Відправлення за номером \
RB193328726HK передано 04.08.2010 в об'єкт поштового зв'язку \
ДНІПРОПЕТРОВСЬК 69 з індексом 49069, на даний час не вручене."}, info)

    def test_filial_info_parsing(self):
        f = open(os.path.join(os.getcwd(), 'test/html/49069.html'), 'r')
        html = f.read()
        f.close()

        parsed = parse_filial_info(html, u"Дніпропетровськ")

        self.assertEqual(u"Дніпропетровськ", parsed['place'])
        self.assertEqual(u"вул. Г. Сталінграда, 8", parsed['street'])
        self.assertEqual("749-69-92", parsed['phone'])

        self.assertEqual(u'Відділення поштового зв\'язку № 69 м. \
Дніпропетровськ Поштамту - ЦПЗ № 1 Дніпропетровської дирекції \
Українського державного підприємства поштового зв\'язку "Укрпошта"',
        parsed['address_full'])

    def test_empty_filial(self):
        with open(os.path.join(os.getcwd(), 'test/html/filial_empty.html'), 'r') as f:
            html = f.read()

        code, place = parse_filial_searchresult(html)
        self.assertEqual(False, place)
        self.assertEqual(False, code)

    def test_filial_code_place(self):
        with open(os.path.join(os.getcwd(), 'test/html/index_search.html'), 'r') as f:
            html = f.read()

        code, place = parse_filial_searchresult(html)
        self.assertEqual(u"Дніпропетровськ", place)
        self.assertEqual(32000100227819, code)

    def test_filial_code_place_31000(self):
        with open(os.path.join(os.getcwd(), 'test/html/index_search_31000.html'), 'r') as f:
            html = f.read()

        code, place = parse_filial_searchresult(html)
        self.assertEqual(32000100524043, code)
        self.assertEqual(u"Слобідка Красилівська", place)

    def test_unicode_comparison(self):
        f = open(os.path.join(os.getcwd(), 'test/unicode.txt'), 'r')
        u = f.read().strip()
        f.close()
        self.assertEqual("привет!", u)


if __name__ == '__main__':
    unittest.main()

