'''
Main application file
TODO https://github.com/Nixellion/flask_boilerplate/issues
'''

ASYNC_MODE = "gevent"  # gevent, eventlet

if ASYNC_MODE == 'eventlet':
    import eventlet

    eventlet.monkey_patch()
elif ASYNC_MODE == "gevent":
    from gevent import monkey

    monkey.patch_all()

from flask import Flask, Response, render_template, Markup, request, redirect
# from flask.ext.assets import Environment, Bundle
from flask_socketio import SocketIO

from datetime import datetime

# region Logger
from debug import get_logger
log = get_logger("default")
# endregion

from configuration import read_config
import jinja_filters

config = read_config()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BLAAAA_GeneerateMeDynamicallyForBetterSecurity'

socketio = SocketIO(app, async_mode=ASYNC_MODE)

app.jinja_env.filters['html_line_breaks'] = jinja_filters.html_line_breaks


@app.context_processor
def inject_global_variables():
    return dict(
        config=config,
        now=datetime.now()
    )


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
        if config['server'].get('host', '0.0.0.0') == "0.0.0.0":
            host = 'localhost'
        else:
            host = config['server']['host']
        log.info(f"Running at http://{host}:{config['server']['port']}")
        socketio.run(app, **config['server'])
    except:
        log.error("Unable to start", exc_info=True)
