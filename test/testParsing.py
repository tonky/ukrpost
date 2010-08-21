#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys, os 
sys.path.append(os.getcwd()) 
from post import delivery_info, filial_info

class TestHtmlParsing(unittest.TestCase):
    def test_delivery(self):
        f = open(os.path.join(os.getcwd(), 'test/barcode.html'), 'r')
        html = f.read()
        f.close()

        info = delivery_info(html)

        self.assertEqual({'zipcode': 49069, 'updated': '04.08.2010', 
            'status_full': "Відправлення за номером \
RB193328726HK передано 04.08.2010 в об'єкт поштового зв'язку \
ДНІПРОПЕТРОВСЬК 69 з індексом 49069, на даний час не вручене."}, info)

    def test_filial_info_parsing(self):
        f = open(os.path.join(os.getcwd(), 'test/details.html'), 'r')
        html = f.read()
        f.close()

        parsed = filial_info(html)

        self.assertEqual(u"вул. Г. Сталінграда, 8", parsed['street'])
        self.assertEqual("749-69-92", parsed['phone'])

        self.assertEqual(u'Відділення поштового зв\'язку № 69 м. \
Дніпропетровськ Поштамту - ЦПЗ № 1 Дніпропетровської дирекції \
Українського державного підприємства поштового зв\'язку "Укрпошта"',
        parsed['address_full'])


    def test_unicode_comparison(self):
        f = open(os.path.join(os.getcwd(), 'test/unicode.txt'), 'r')
        u = f.read().strip()
        f.close()
        self.assertEqual("привет!", u)


if __name__ == '__main__':
    unittest.main()

