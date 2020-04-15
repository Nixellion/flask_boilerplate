'''
Main application file
'''

import eventlet
eventlet.monkey_patch()

from flask import Flask, Response, render_template, Markup, request, redirect
from flask_socketio import SocketIO

# region Logger
import logging
from debug import setup_logging

log = logger = logging.getLogger("default")
setup_logging()
# endregion

from configuration import read_config
import bro_jinja

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BLAAAA_GeneerateMeDynamicallyForBetterSecurity'

socketio = SocketIO(app, async_mode='eventlet')


app.jinja_env.filters['html_line_breaks'] = bro_jinja.html_line_breaks
#
# @app.context_processor
# def inject_global_variables():
#     return dict(
#         GetData=GetData()
#     )


def add_background_task(task, interval):
    def tsk():
        while True:
            try:
                log.debug(f"Running background task {task.__name__}...")
                task()
                log.debug(f"Completed background task {task.__name__}!")
            except Exception as e:
                log.error(f"Can't run background task '{task.__name__}': {e}", exc_info=True)
            socketio.sleep(interval)

    socketio.start_background_task(tsk)


if __name__ == '__main__':
    
    # add_background_task(log_chat, 5)
    config = read_config()

    from views import app as views
    from api import app as api
    app.register_blueprint(views)
    app.register_blueprint(api)

    try:
        log.info(f"Running at {config['host']}:{config['port']}")
        socketio.run(app, debug=False, host=config['host'], port=config['port'])
    except:
        print("Unable to start", exc_info=True)



