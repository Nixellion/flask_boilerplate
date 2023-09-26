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

from flask import Flask
# from flask.ext.assets import Environment, Bundle
from flask_socketio import SocketIO

from functools import partial

from datetime import datetime

# region Logger
from loguru import logger as log
# endregion

from configuration import read_config
from utilities.jinja_utils import common_filters, common_globals

config = read_config()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Please-Change-This-For-Better-Security-19#91-Or-Generate-Dynamically'

socketio = SocketIO(app, async_mode=ASYNC_MODE)

for filter_function in common_filters.enabled_filters:
    app.jinja_env.filters[filter_function.__name__] = filter_function


@app.context_processor
def inject_global_variables():
    global_vars = dict(
        config=config,
        now=datetime.now()
    )

    for func in common_globals.enabled_functions:
        global_vars[func.__name__] = func

    return global_vars


def add_background_task(task, interval):
    def tsk():
        while True:
            try:
                if isinstance(task, partial):
                    log.debug(f"Running background task {task.func.__name__}...")
                    task()
                    log.debug(f"Completed background task {task.func.__name__}!")
                else:
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

    from routes.views import app as views
    from routes.api import app as api

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
