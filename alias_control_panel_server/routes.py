from app import app, session_store
from flask import request, jsonify

from utils import *
from models import UserSession

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

        session.close()
        session_store.remove(session)
        return res
    else:
        return create_unauthorized_response("You are not authorized")

@app.route("/get-speakers", methods=['GET'])
def get_speakers():
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

        res = create_success_response(content=jsonify([ s.__dict__ for s in session.get_speakers() ]))

        return res
    else:
        return create_unauthorized_response("You are not authorized")

@app.route("/change-speaker", methods=['POST', 'OPTIONS'])
def change_speaker():
    if request.method == "OPTIONS":
        return create_success_response()

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

        new_speaker = request.json
        session.change_active_speaker(new_speaker)

        res = create_success_response(content=jsonify([s.__dict__ for s in session.get_speakers()]))

        return res
    else:
        return create_unauthorized_response("You are not authorized")

@app.route("/play-music", methods=['GET', 'POST', 'OPTIONS'])
def play_music():
    if request.method == "OPTIONS":
        return create_success_response()

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

        if request.method == "GET":
            session.play_music()
        elif request.method == "POST":
            session.play_music(**request.json)

        return create_success_response()
    else:
        return create_unauthorized_response("You are not authorized")

@app.route("/stop-music", methods=['GET'])
def stop_music():
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

        session.stop_music()

        return create_success_response()
    else:
        return create_unauthorized_response("You are not authorized")
