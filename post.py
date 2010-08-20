#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import re
from BeautifulSoup import BeautifulSoup

filial_info_url = "http://services.ukrposhta.com/postindex_new/details.aspx?postfilial=%i"

viewstate = """/wEPDwUJNjEyMzA2MTk3D2QWAmYPZBYCAgMPZBYEAgEPDxYEHgtOYXZpZ2F0ZVVybAUMSGVscF91bC5hc3B4HgRUZXh0BQ7QlNC+0LLRltC00LrQsGRkAgUPZBYOAgMPZBYCZg9kFgICAQ8PFgIfAQUFNDkwNjlkZAIHD2QWAmYPZBYCAgEPEA8WAh4LXyFEYXRhQm91bmRnZBAVHB3QntCx0LXRgNGW0YLRjCDQvtCx0LvQsNGB0YLRjBLQktGW0L3QvdC40YbRjNC60LAS0JLQvtC70LjQvdGB0YzQutCwINCU0L3RltC/0YDQvtC/0LXRgtGA0L7QstGB0YzQutCwENCU0L7QvdC10YbRjNC60LAW0JbQuNGC0L7QvNC40YDRgdGM0LrQsBjQl9Cw0LrQsNGA0L/QsNGC0YHRjNC60LAU0JfQsNC/0L7RgNGW0LfRjNC60LAh0IbQstCw0L3Qvi3QpNGA0LDQvdC60ZbQstGB0YzQutCwCNCa0LjRl9CyENCa0LjRl9Cy0YHRjNC60LAc0JrRltGA0L7QstC+0LPRgNCw0LTRgdGM0LrQsBLQm9GD0LPQsNC90YHRjNC60LAS0JvRjNCy0ZbQstGB0YzQutCwGNCc0LjQutC+0LvQsNGX0LLRgdGM0LrQsA7QntC00LXRgdGM0LrQsBTQn9C+0LvRgtCw0LLRgdGM0LrQsB3QoNC10YHQv9GD0LHQu9GW0LrQsCDQmtGA0LjQvBTQoNGW0LLQvdC10L3RgdGM0LrQsBbQodC10LLQsNGB0YLQvtC/0L7Qu9GMDtCh0YPQvNGB0YzQutCwGtCi0LXRgNC90L7Qv9GW0LvRjNGB0YzQutCwFNCl0LDRgNC60ZbQstGB0YzQutCwFNCl0LXRgNGB0L7QvdGB0YzQutCwFtCl0LzQtdC70YzQvdC40YbRjNC60LAS0KfQtdGA0LrQsNGB0YzQutCwFtCn0LXRgNC90ZbQstC10YbRjNC60LAY0KfQtdGA0L3RltCz0ZbQstGB0YzQutCwFRwACTUwMDAwMDAwMAk1MDAwMDAwMDEJNTAwMDAwMDAzCTUwMDAwMDAwNAk1MDAwMDAwMDUJNTAwMDAwMDA2CTUwMDAwMDAwNwk1MDAwMDAwMDgJNTAwMDAwMDA5CTUwMDAwMDAxMAk1MDAwMDAwMTEJNTAwMDAw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"""

def filial_html(code):
    """Gets filial html by internal code
    """

    url = 'http://services.ukrposhta.com/postindex_new/details.aspx?postfilial=%s' % code

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    return html

def filial_info(html):
    """Parses html from UP filial details page and returns description, local 
    address and phone number

    >>> f = open('/media/storage/projects/ukrpost/test/details.html', 'r')
    >>>	html = f.read()
    >>> f.close()
    >>> filial_info(html)
    [u'\u0412\u0456\u0434\u0434\u0456\u043b\u0435\u043d\u043d\u044f \u043f\u043e\u0448\u0442\u043e\u0432\u043e\u0433\u043e \u0437\u0432\\'\u044f\u0437\u043a\u0443 \u2116 69 \u043c. \u0414\u043d\u0456\u043f\u0440\u043e\u043f\u0435\u0442\u0440\u043e\u0432\u0441\u044c\u043a \u041f\u043e\u0448\u0442\u0430\u043c\u0442\u0443 - \u0426\u041f\u0417 \u2116 1 \u0414\u043d\u0456\u043f\u0440\u043e\u043f\u0435\u0442\u0440\u043e\u0432\u0441\u044c\u043a\u043e\u0457 \u0434\u0438\u0440\u0435\u043a\u0446\u0456\u0457 \u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u043e\u0433\u043e \u0434\u0435\u0440\u0436\u0430\u0432\u043d\u043e\u0433\u043e \u043f\u0456\u0434\u043f\u0440\u0438\u0454\u043c\u0441\u0442\u0432\u0430 \u043f\u043e\u0448\u0442\u043e\u0432\u043e\u0433\u043e \u0437\u0432\\'\u044f\u0437\u043a\u0443 "\u0423\u043a\u0440\u043f\u043e\u0448\u0442\u0430"', u'\u0432\u0443\u043b. \u0413. \u0421\u0442\u0430\u043b\u0456\u043d\u0433\u0440\u0430\u0434\u0430, 8', u'749-69-92']
    """

    fullname = address = phone = ""


    html = re.sub('&quot;', '"', html)

    soup = BeautifulSoup(html, fromEncoding="utf-8", smartQuotesTo=None)

    fullname = soup.find("table", id='ctl00_ContentPlaceHolder1_dw').find('td').nextSibling.string

    address = soup.find("table", 
        id='ctl00_ContentPlaceHolder1_dw').findAll('tr')[1].find('td').nextSibling.string

    phone = soup.find("table", 
        id='ctl00_ContentPlaceHolder1_dw').findAll('tr')[2].find('td').nextSibling.string

    return [fullname, address, phone]

def barcode_search_html(barcode):
    """Get html of barcode search page

    >>> delivery_info(barcode_search_html("RB193328726HK"))
    [49069, '04.08.2010', 'The item number RB193328726HK was sent to the postal \
facility DNIPROPETROVSK 69, the postcode 49069, on 04.08.2010, but it has not \
been handed over to the addressee.']
    """

    search_barcode_url = 'http://80.91.187.254:8080/servlet/SMCSearch2?&lang=en&barcode=%s' % barcode

    f = urllib.urlopen(search_barcode_url)
    html = f.read()
    f.close()

    return html

def delivery_info(html):
    """Parse the html file returned by UP barcode search and get filial number
    where the package currently is

    >>> f = open('/media/storage/projects/ukrpost/test/barcode.html', 'r')
    >>>	html = f.read()
    >>> f.close()
    >>> delivery_info(html)
    [49069, '04.08.2010', 'The item number RB193328726HK was sent to the postal \
facility DNIPROPETROVSK 69, the postcode 49069, on 04.08.2010, but it has not \
been handed over to the addressee.']
    """

    # strip excess whitespace and tags, also stupid windown newlines
    html = re.sub('\r', '', html)
    html = re.sub('\n', '', html)
    html = re.sub('<.*?>', '', html)
    html = re.sub('\s+', ' ', html)

    re_code = re.search('the postcode (\d+)', html)
    code = int(re_code.group(1))

    re_date = re.search('on (\d\d\.\d\d\.\d{4})', html)
    date = re_date.group(1)

    re_info = re.search('(The item .*\.)\s', html, re.S)
    info = re_info.group(1)

    return [code, date, info]

def filial_search_html(index):
    """Get html with index search result

    >>> filial_code(filial_search_html(49020))
    33000000597035
    """
    
    search_post_url = 'http://services.ukrposhta.com/postindex_new/default_ul.aspx'
    search_post_args = { '__VIEWSTATE': viewstate }
    params = urllib.urlencode(search_post_args)
    params2 = params + "&ctl00$ContentPlaceHolder1$txtIndex=%i" % index

    f = urllib.urlopen(search_post_url, params2)
    html = f.read()
    f.close()

    return html

def filial_code(html):
    """Parse the html file returned by UP search API and get internal filial identifier

    >>> f = open('/media/storage/projects/ukrpost/test/index_search.html', 'r')
    >>>	html = f.read()
    >>> f.close()
    >>> filial_code(html)
    32000100227819
    """

    soup = BeautifulSoup(html)
    code = soup.find(attrs={'href' : re.compile("postfilial")})['href'].split('=')[1]

    return int(code)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
