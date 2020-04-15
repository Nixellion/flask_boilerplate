'''
HTML template views, actualy website frontend stuff
Could use flask-restful, I personally did not find much benefit in using it, yet.
'''

import os
from flask import Blueprint, render_template, request, redirect, Response, jsonify, send_from_directory
from debug import catch_errors_html
from paths import APP_DIR

app = Blueprint("views", __name__)

@app.route("/")
@catch_errors_html
def index():
    return render_template("index.html", some_variable=APP_DIR)

@app.route("/download/<var1>/<var2>")
@catch_errors_html
def dl(var1, var2):
    return send_from_directory(os.path.join(APP_DIR, var1), os.path.join(APP_DIR, var1, var2))

