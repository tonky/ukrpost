#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is the API to get Ukrpost package tracking status, including address of the
place package is currently in. I'm not aware of Ukrpost API for this, so all the
information is aquired by parsing html from their respective webpages. Results
are cached and address of filial with the package is geocoded, then all this
information is returned as json, for frontend to display.
"""

from BeautifulSoup import BeautifulSoup
import re
import urllib
from geocode import geocode
from cache import cache

try:
    import json
except ImportError:
    import simplejson as json


@cache() # cache indefinitely on empty argument
def index(zipcode):
    "Returns filial information in json by its zipcode"

    code, place = parse_filial_searchresult(filial_search_html(int(zipcode)))

    if not code:
        return False

    info = json.dumps(parse_filial_info(filial_info(code), place))

    return info

@cache(300) # cache for given number of minutes
def track(number):
    "Returns tracking package location and current filial information"

    delivery = parse_tracking_search(tracking_search(number))

    # dummy data
    if number == 'AA111111111BB':
        delivery = {'zipcode': 34020, 'updated': '23.09.2010', 
            'status_full': "Відправлення за номером \
AA111111111BB передано 20.09.2010 в об'єкт поштового зв'язку \
Неньковичи з індексом 34020, на даний час не вручене."}

    if number == 'AA222222222BB':
        delivery = {'zipcode': 27240, 'updated': '23.09.2010', 
            'status_full': "Відправлення за номером \
AA222222222BB передано 20.09.2010 в об'єкт поштового зв'язку \
Тарасівка з індексом 27240, на даний час не вручене."}

    if number == 'AA333333333BB':
        delivery = {'zipcode': 19120, 'updated': '23.09.2010', 
            'status_full': "Відправлення за номером \
AA333333333BB передано 20.09.2010 в об'єкт поштового зв'язку \
Шарнопіль з індексом 19120, на даний час не вручене."}

    if not delivery:
        return False

    code, place = parse_filial_searchresult(filial_search_html(delivery['zipcode']))

    if not code:
        return False

    filial = parse_filial_info(filial_info(code), place)

    delivery.update(filial)

    return json.dumps(delivery)


# #############################################################################
# Helper API functions, should not be directly called by package users

# to get filial search data we have to submit this in POST
viewstate = """/wEPDwUJNjEyMzA2MTk3D2QWAmYPZBYCAgMPZBYEAgEPDxYEHgtOYXZpZ2F0ZVVybAUMSGVscF91bC5hc3B4HgRUZXh0BQ7QlNC+0LLRltC00LrQsGRkAgUPZBYOAgMPZBYCZg9kFgICAQ8PFgIfAQUFNDkwNjlkZAIHD2QWAmYPZBYCAgEPEA8WAh4LXyFEYXRhQm91bmRnZBAVHB3QntCx0LXRgNGW0YLRjCDQvtCx0LvQsNGB0YLRjBLQktGW0L3QvdC40YbRjNC60LAS0JLQvtC70LjQvdGB0YzQutCwINCU0L3RltC/0YDQvtC/0LXRgtGA0L7QstGB0YzQutCwENCU0L7QvdC10YbRjNC60LAW0JbQuNGC0L7QvNC40YDRgdGM0LrQsBjQl9Cw0LrQsNGA0L/QsNGC0YHRjNC60LAU0JfQsNC/0L7RgNGW0LfRjNC60LAh0IbQstCw0L3Qvi3QpNGA0LDQvdC60ZbQstGB0YzQutCwCNCa0LjRl9CyENCa0LjRl9Cy0YHRjNC60LAc0JrRltGA0L7QstC+0LPRgNCw0LTRgdGM0LrQsBLQm9GD0LPQsNC90YHRjNC60LAS0JvRjNCy0ZbQstGB0YzQutCwGNCc0LjQutC+0LvQsNGX0LLRgdGM0LrQsA7QntC00LXRgdGM0LrQsBTQn9C+0LvRgtCw0LLRgdGM0LrQsB3QoNC10YHQv9GD0LHQu9GW0LrQsCDQmtGA0LjQvBTQoNGW0LLQvdC10L3RgdGM0LrQsBbQodC10LLQsNGB0YLQvtC/0L7Qu9GMDtCh0YPQvNGB0YzQutCwGtCi0LXRgNC90L7Qv9GW0LvRjNGB0YzQutCwFNCl0LDRgNC60ZbQstGB0YzQutCwFNCl0LXRgNGB0L7QvdGB0YzQutCwFtCl0LzQtdC70YzQvdC40YbRjNC60LAS0KfQtdGA0LrQsNGB0YzQutCwFtCn0LXRgNC90ZbQstC10YbRjNC60LAY0KfQtdGA0L3RltCz0ZbQstGB0YzQutCwFRwACTUwMDAwMDAwMAk1MDAwMDAwMDEJNTAwMDAwMDAzCTUwMDAwMDAwNAk1MDAwMDAwMDUJNTAwMDAwMDA2CTUwMDAwMDAwNwk1MDAwMDAwMDgJNTAwMDAwMDA5CTUwMDAwMDAxMAk1MDAwMDAwMTEJNTAwMDAw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"""

def filial_info(code):
    "Gets filial html by internal code"

    url = 'http://services.ukrposhta.com/postindex_new/details.aspx?postfilial=%s' % code

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    return html

def parse_filial_info(html, place):
    """Parses html from UP filial details page and returns description, local 
    address and phone number
    """

    fullname = address = phone = ""
    town = city = village = coords = ""


    html = re.sub('&quot;', '"', html)

    soup = BeautifulSoup(html, fromEncoding="utf-8")

    fullname = soup.find("table", id='ctl00_ContentPlaceHolder1_dw').find('td').nextSibling.string

    address = soup.find("table", 
        id='ctl00_ContentPlaceHolder1_dw').findAll('tr')[1].find('td').nextSibling.string

    phone = soup.find("table", 
        id='ctl00_ContentPlaceHolder1_dw').findAll('tr')[2].find('td').nextSibling.string

    coords = geocode(place, address)

    return {'address_full': fullname, 'street': address, 'phone': phone, 
            'place': place, 'coordinates': coords}

def tracking_search(barcode):
    "Get html of barcode search page"

    search_barcode_url = 'http://80.91.187.254:8080/servlet/SMCSearch2?&lang=ua&barcode=%s' % barcode

    f = urllib.urlopen(search_barcode_url)
    html = f.read()
    f.close()

    return html

def parse_tracking_search(html):
    """Parse the html file returned by UP barcode search and get filial number
    where the package currently is
    """

    date = ""

    # strip excess whitespace and tags, also stupid windows newlines
    html = re.sub('\r', '', html)
    html = re.sub('\n', '', html)
    html = re.sub('<.*?>', '', html)
    html = re.sub('\s+', ' ', html)

    re_code = re.search('з індексом (\d+)', html)

    if not re_code:
        return False

    code = int(re_code.group(1))

    # moved to filial
    transfer_date = re.search('передано (\d\d\.\d\d\.\d{4})', html)

    # registered at filial, and being processed
    register_date = re.search('зареєстроване (\d\d\.\d\d\.\d{4})', html)

    if transfer_date:
        date = transfer_date.group(1)

    if register_date:
        date = register_date.group(1)

    re_info = re.search('(Відправлення .*\.)\s', html, re.S)
    info = re_info.group(1)

    return {'zipcode': code, 'updated': date, 'status_full': info}

def filial_search_html(index):
    """Get html with index search result
    """
    
    search_post_url = 'http://services.ukrposhta.com/postindex_new/default_ul.aspx'
    search_post_args = { '__VIEWSTATE': viewstate }
    params = urllib.urlencode(search_post_args)
    params2 = params + "&ctl00$ContentPlaceHolder1$txtIndex=%i" % index

    f = urllib.urlopen(search_post_url, params2)
    html = f.read()
    f.close()

    return html

def parse_filial_searchresult(html):
    """Parse the html file returned by UP search API and get internal filial identifier
    """

    if not html:
        return (False, False)

    soup = BeautifulSoup(html, fromEncoding="utf-8")
    code = soup.find(attrs={'href' : re.compile("postfilial")})

    if not code:
        return (False, False)

    code = code['href'].split('=')[1]

    place = soup.find(id="ctl00_ContentPlaceHolder1_dgResult").find("tr").nextSibling.find("td").nextSibling.nextSibling.nextSibling.string

    return int(code), place
