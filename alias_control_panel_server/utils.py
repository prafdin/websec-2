from flask import make_response

headers = {
    "Content-Type": "text/plain",
    'Server': 'Foobar',
    'Access-Control-Allow-Origin': 'http://localhost:8080',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Request-Headers': 'Origin, Content-Type, Accept'
}

def set_headers(response):
    for k, v in headers.items():
        response.headers[k] = v

def create_unauthorized_response(content=""):
    r = make_response(content)
    set_headers(r)
    r.status_code = 401
    return r

def create_success_response(content=""):
    r = make_response(content)
    set_headers(r)
    r.status_code = 200
    return r

def check_authorization(cookie_string):
    return True