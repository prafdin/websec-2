from flask import Flask, request, redirect, url_for, jsonify

from utils import *
from yandex_api import YandexAPI

# for run in powershell: flask --app main --debug run
app = Flask(__name__)

users_sessions = []

@app.route('/auth', methods=['GET'])
def authorize():
    if (request.cookies.get('csrf_token')):
        return create_success_response()
    else:
        if request.method == 'GET':
            args = request.args
            username = args.get('login')
            password = args.get('password')

            try:
                api = YandexAPI(username, password)
            except RuntimeError as err:
                return create_unauthorized_response(str(err))

        res = create_success_response()

        day_in_seconds = 60 * 60 * 24
        res.set_cookie('csrf_token', api.csrf_token, max_age=day_in_seconds)

        users_sessions.append(api)

        return res


@app.route("/logout", methods=['GET'])
def logout():
    if (not request.cookies.get('csrf_token') or not check_authorization(request.cookies.get('csrf_token'))):
        return create_unauthorized_response()
    else:
        res = create_success_response()

        res.set_cookie('csrf_token', '', max_age=0)

        session = get_session(request.cookies.get('csrf_token'))
        if session is not None:
            users_sessions.remove(session)

        return res

@app.route("/get_speakers", methods=['GET'])
def get_speakers():
    if (request.cookies.get('csrf_token')):
        if not check_authorization("123"): # TODO
            return redirect(url_for('logout'))

        session = get_session(request.cookies.get('csrf_token'))
        if session is None:
            return redirect(url_for('logout'))

        print(session.get_speakers().__class__)

        return create_success_response(jsonify(session.get_speakers()))
    else:
        return create_success_response()

def get_session(token):
    return next(filter(lambda x: x.csrf_token == token, users_sessions), None)