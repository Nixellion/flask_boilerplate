'''
API paths, manually generated
Could use flask-restful, I personally did not find much benefit in using it, yet.
'''

import os
import time


from flask import Blueprint, jsonify, request, Response
from debug import catch_errors_json
from pygtail import Pygtail

from database import Entry

from paths import LOGS_DIR

app = Blueprint("api", __name__)


def api_response(data=None, success: bool = True, message: str = None):
    """
    Wrapper для API ответов, который помогает легко форматировать данные в едином виде.
    По умолчанию возвращает success
    """
    r = {"success": success}
    if data:
        r['data'] = data
    if message:
        r['message'] = message
    return jsonify(r)


@app.route("/api")
@catch_errors_json
def api_index():
    return jsonify({"data": 123})

@app.route("/api/new_entry", methods=["GET", "POST"])
@catch_errors_json
def api_new_entry():
    if request.method == "POST":
        new_entry = Entry()
        new_entry.filename = request.form['filename']
        new_entry.save()
        return jsonify({"success": True})

@app.route('/api/log_stream')
def log_stream():
    def generate():
        for line in Pygtail(os.path.join(LOGS_DIR, "debug.log"), every_n=1):
            yield "data:" + str(line) + "\n\n"
            time.sleep(0.3)
    return Response(generate(), mimetype='text/event-stream')

# @app.route("/update")
# @catch_errors_json
# def update():
#     var = request.args.get("count", None)
#     if not var:
#         return Response("<b>NEED COUNT</b>")
#
# @app.route("/add_user", methods=["GET", "POST"])
# @catch_errors_json
# def add_user():
#     if request.method == "GET":
#         return render_template("user_list.html")
#     elif request.method == "POST":
#         username = request.form.get('username')


