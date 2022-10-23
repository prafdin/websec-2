from flask import Flask, make_response, request

app = Flask(__name__)


@app.route('/auth', methods=['GET'])
def authorize():
    headers = {
        "Content-Type": "text/plain",
        'Server': 'Foobar',
        'Access-Control-Allow-Origin': 'http://localhost:8080',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Request-Headers': 'Origin, Content-Type, Accept'
    }

    if (request.cookies.get('login-token')):
        r = make_response()
        for k, v in headers.items():
            r.headers[k] = v
        r.status_code = 200
        return r
    else:
        if request.method == 'GET':
            args = request.args
            username = args.get('login')
            password = args.get('password')

            if username != 'root' or password != 'root':
                r = make_response()
                for k, v in headers.items():
                    r.headers[k] = v
                r.status_code = 401
                return r

        day_in_seconds = 60 * 60 * 24
        res = make_response("Setting a cookie")
        for k, v in headers.items():
            res.headers[k] = v
        res.set_cookie('login-token', '123456789', max_age=day_in_seconds)
        return res