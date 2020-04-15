'''
API paths, manually generated
Could use flask-restful, I personally did not find much benefit in using it, yet.
'''


from flask import Blueprint, jsonify
from debug import catch_errors_json


app = Blueprint("api", __name__)

@app.route("/api")
@catch_errors_json
def api_index():
    return jsonify({"data": 123})


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


