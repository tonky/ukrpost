from wsgiref.simple_server import make_server
from post import filial_search_html, filial_code, filial_info, filial_html, delivery_info, barcode_search_html
import re
import os

try:
    import json
except ImportError:
    import simplejson as json

def ukrpost(environ, start_response):
    path = environ['PATH_INFO']

    if path == "/":
        return html(start_response)

    status = '200 OK'
    headers = [('Content-type', 'application/json'), ('charset','utf-8')]
    start_response(status, headers)

    if path == "/help":
        return help()

    urls = path[1:].partition("/")

    if urls[0] == "index":
        return index(urls[2])

    if urls[0] == "track":
        return track(urls[2])

    return help()

def html(start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html'), ('charset','utf-8')]
    start_response(status, headers)

    f = open(os.path.join(os.getcwd(), 'index.html'), 'r')
    html = f.read()
    f.close()

    return html

def index(index):
    code = filial_code(filial_search_html(int(index)))
    info = filial_info(filial_html(code))
    return [json.dumps(info)]

def track(code):
    delivery= delivery_info(barcode_search_html(code))

    code = filial_code(filial_search_html(delivery[0]))
    filial = filial_info(filial_html(code))

    delivery.extend(filial)

    return [json.dumps(delivery)]

def help():
    return "/index/49069 for post office info<br> \
/track/xxxxxxxxxxxxxxxx for full tracking info"

httpd = make_server('', 8000, ukrpost)
print "Serving on port 8000..."

# Serve until process is killed
httpd.serve_forever()
