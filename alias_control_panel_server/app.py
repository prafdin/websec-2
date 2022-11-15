from flask import Flask, send_from_directory
from store import SessionStore
from config import app_config

# for run in powershell: flask --app app --debug run
app = Flask(__name__, static_folder=app_config.SITE_ROOT)
session_store = SessionStore()

from routes import *

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')  # give routing responsibility to vue router
def index(path):
    return app.send_static_file("index.html")

@app.route('/static/<path:path>')
def static_dist(path):
    return send_from_directory(
        app_config.SITE_ROOT + "\\static", path)


if __name__ == '__main__':
    app.run(debug=True)