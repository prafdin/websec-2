from flask import Flask, request, redirect, url_for, jsonify
from store import SessionStore

# for run in powershell: flask --app app --debug run
app = Flask(__name__)
session_store = SessionStore()


from routes import *

if __name__ == '__main__':
    app.run(debug=True)