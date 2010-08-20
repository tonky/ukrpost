from wsgiref.simple_server import make_server
from post import filial_search_html, filial_code, filial_info, filial_html, delivery_info, barcode_search_html
import json
import re

def ukrpost(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'application/json')] # HTTP Headers
    start_response(status, headers)

    path = environ['PATH_INFO']

    if path == "/":
        return help()

    urls = path[1:].partition("/")

    if urls[0] == "index":
        return index(urls[2])

    if urls[0] == "track":
        return track(urls[2])

    return help()

def index(index):
    code = filial_code(filial_search_html(int(index)))
    info = filial_info(filial_html(code))
    return [json.dumps(info)]

def track(code):
    info = delivery_info(barcode_search_html(code))
    return [json.dumps(info)]

def help():
    return "/index/49069 for post office info<br> \
/track/xxxxxxxxxxxxxxxx for full tracking info"

httpd = make_server('', 8000, ukrpost)
print "Serving on port 8000..."

# Serve until process is killed
httpd.serve_forever()
