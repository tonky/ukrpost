from wsgiref.simple_server import make_server
from post import filial_search_html, filial_code, filial_info, filial_html, delivery_info, barcode_search_html
import re
import os

try:
    import json
except ImportError:
    import simplejson as json

def ukrpost(environ, start_response):
    # dispatch request, distinguishing between static and dynamic
    # make sure content-types are matching and charset is set
    # return 404 on missing static, file with guessed contenttype otherwise
    # known path

    path = environ['PATH_INFO']

    # default content-type, status and response
    ctype = 'text/plain'
    status = '200 OK'
    body = False
    charset = 'utf-8'

    if re.match("/index/(\d+)", path):
        ctype, body = index(path[1:].partition("/")[2])

    if re.match("/track/(\w+)", path):
        ctype, body = track(path[1:].partition("/")[2])

    if path == "/":
        path = "/index.html"

    if not body:
        ctype, body = static(path[1:])

    if not body:
        status = '404 Not found'
        body = "Not found"

    headers = [('Content-type', ctype), ('charset', charset)]
    start_response(status, headers)

    return body

def static(path):
    ctype = 'text/plain'

    if re.search("\.html", path):
        ctype = 'text/html'

    if re.search("\.css", path):
        ctype = 'text/css'

    if re.search("\.js", path):
        ctype = 'application/javascript'

    try:
        f = open(os.path.join(os.getcwd(), path), 'r')
        body = f.read().strip()
        f.close()
    except:
        body = False

    return ctype, body

def index(index):
    code, place = filial_code(filial_search_html(int(index)))
    info = filial_info(filial_html(code), place)
    return "application/json", json.dumps(info)

def track(code):
    delivery= delivery_info(barcode_search_html(code))

    code, place = filial_code(filial_search_html(delivery['zipcode']))
    filial = filial_info(filial_html(code), place)

    delivery.update(filial)

    return "application/json", json.dumps(delivery)

def help():
    return "/index/49069 for post office info<br> \
/track/xxxxxxxxxxxxxxxx for full tracking info"

def run():
    httpd = make_server('', 8000, ukrpost)
    print "Serving on port 8000..."

    # Serve until process is killed
    httpd.serve_forever()

def run_once():
    httpd = make_server('', 8000, ukrpost)
    print "Serving on port 8000..."

    httpd.handle_request()


if __name__ == '__main__':
    run()
