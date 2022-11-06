from flask import make_response

headers = {
    "Content-Type": "text/plain",
    'Server': 'Foobar',
    'Access-Control-Allow-Origin': 'http://localhost:8080',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
}

def create_unauthorized_response(content=""):
    r = make_response(content)
    r.headers.update(headers)
    r.status_code = 401
    return r

def create_success_response(content=""):
    r = make_response(content)
    r.headers.update(headers)
    r.status_code = 200
    return r