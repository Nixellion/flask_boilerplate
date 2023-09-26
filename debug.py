import traceback
import functools

from flask import Response, jsonify, render_template

# region Logger
import os
from loguru import logger as log
message_level = log.level("MSG", no=25, color="<magenta>", icon="🐍")
project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
log.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs", f"{project_name}.log"), rotation="5 MB")
# endregion


def catch_errors(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            log.error(f"Error in function {f.__name__}: {str(e)}", exc_info=True)
            return None
    return wrapped


def catch_errors_json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e), "traceback": traceback.format_exc()})
    return wrapped


def catch_errors_html(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return render_template("error.html", error=str(e), details=traceback.format_exc())
    return wrapped