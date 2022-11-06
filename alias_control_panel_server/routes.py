from app import app, session_store
from flask import Flask, request, redirect, url_for, jsonify

from utils import *
from models import UserSession
from yandex_api import YandexAPI

@app.route('/auth', methods=['GET'])
def authorize():
    token = request.cookies.get(UserSession.token_name)
    if (token):
        session = session_store.get_session(token)
        if not session:
            response = create_unauthorized_response("Session for this user doesn't exist")
            response.set_cookie(UserSession.token_name, '', max_age=0)
            return response

        if not session.check():
            response = create_unauthorized_response("Session for this user expired")
            response.set_cookie(UserSession.token_name, '', max_age=0)
            session_store.remove(session)
            return response

        return create_success_response()
    else:
        username = request.args.get('login')
        password = request.args.get('password')
        try:
            session = UserSession(username, password)
        except RuntimeError as err:
            return create_unauthorized_response(str(err))

        res = create_success_response()
        res.set_cookie(UserSession.token_name, session.token, max_age=60 * 60 * 24)

        session_store.append(session)
        return res


@app.route("/logout", methods=['GET'])
def logout():
    token = request.cookies.get(UserSession.token_name)
    if (token):
        session = session_store.get_session(token)
        if not session:
            response = create_unauthorized_response("Session for this user doesn't exist")
            response.set_cookie(UserSession.token_name, '', max_age=0)
            return response

        res = create_success_response()
        res.set_cookie(UserSession.token_name, '', max_age=0)

        session_store.remove(session)
        return res
    else:
        return create_unauthorized_response("You are not authorized")

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

devices = [
    {
      "image": "https://yastatic.net/s3/frontend/quasar/_/3624d5019c8d9b6d9601486da6c01bf3.png",
      "name": 'Yandex Sasisa',
      "used": True
    },
    {
      "image": 'https://yastatic.net/s3/frontend/quasar/_/3624d5019c8d9b6d9601486da6c01bf3.png',
      "name": 'Yandex Aziza',
      "used": False
    }
  ]


@app.route("/get-devices", methods=['GET'])
def get_devices():

    return create_success_response(content=jsonify(devices))
    # if (request.cookies.get('csrf_token')):
    #     return create_success_response(content=jsonify(devices))
    # else:
    #     return create_success_response()


@app.route("/change-device", methods=['POST', 'OPTIONS'])
def change_device():

    if request.method == "OPTIONS":
        return create_success_response()


    new_device = request.json
    for d in devices:
        if d["name"] == new_device["name"]:
            d["used"] = True
        else:
            d["used"] = False

    return create_success_response(content=jsonify(devices))

def get_session(token):
    return next(filter(lambda x: x.csrf_token == token, users_sessions), None)