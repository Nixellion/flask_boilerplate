__author__ = "Michel Davydov"

import logging
import json
import os
import traceback

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

import threading
import socket

from configuration import PRODUCTION_MODE
from paths import FAILED_SLACK_MESSAGES_FP

hostname = socket.gethostname().strip()


class SlackExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(SlackExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(SlackExceptionFormatter, self).format(record)
        if record.exc_text:
            s = f"\n```\n{s}\n```\n"
        return s


class SlackLogHandler(logging.Handler):
    COLORS = {
        logging.NOTSET: '#757575',
        logging.DEBUG: '#757575',
        logging.INFO: '#7581ff',
        logging.WARNING: '#ffb300',
        logging.ERROR: '#ff1100',
        logging.CRITICAL: '#ff1100'
    }

    EMOJIS = {
        logging.NOTSET: ':loudspeaker:',
        logging.DEBUG: ':speaker:',
        logging.INFO: ':information_source:',
        logging.WARNING: ':warning:',
        logging.ERROR: ':exclamation:',
        logging.CRITICAL: ':boom:'
    }

    def __init__(self, webhook_url, channel=None, username=None, emojis=None, colors=None,
                 format='[%(asctime)s] [%(name)s] \n```\n%(message)s\n```', threaded=True, fallback_webhook_url=None):
        logging.Handler.__init__(self)
        self.webhook_url = webhook_url
        self.fallback_webhook_url = fallback_webhook_url
        self.channel = channel
        self.username = username
        self.emojis = emojis if emojis is not None else SlackLogHandler.EMOJIS
        self.colors = colors if colors is not None else SlackLogHandler.COLORS
        self.formatter = SlackExceptionFormatter(format)
        self.threaded = threaded

    def _make_content(self, record):
        icon_emoji = getattr(record, 'slack_icon', self.emojis[record.levelno])

        attachements = {
            "fallback": self.format(record),
            "title": f"{icon_emoji} {logging.getLevelName(record.levelno)} [{hostname}]",
            "text": self.format(record),
            "color": self.colors[record.levelno]
        }
        content = {
            'text': '',
            'icon_emoji': icon_emoji,
            'attachments': [attachements]
        }
        if hasattr(record, 'slack_username'):
            content['username'] = getattr(record, 'slack_username')
        elif self.username:
            content['username'] = self.username
        else:
            content['username'] = "{0} - {1}".format(record.module, record.name)
        if self.channel:
            content['channel'] = self.channel
        return content

    def emit_wrapped(self, record):
        try:
            try:
                req = Request(self.webhook_url)
                req.add_header('Content-Type', 'application/json')
                req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
                content = self._make_content(record)
                urlopen(req, json.dumps(content).encode("utf-8"))
            except Exception as e:
                req = Request(self.fallback_webhook_url)
                req.add_header('Content-Type', 'application/json')
                content = self._make_content(record)
                content['attachments'][0]['text'] += f"""WEBHOOK FALLBACK REASON: {e}

```
{traceback.format_exc()}
```"""
                urlopen(req, json.dumps(content).encode("utf-8"))

        except Exception as e:
            try:
                with open(FAILED_SLACK_MESSAGES_FP, "a+") as f:
                    f.write(f"{logging.getLevelName(record.levelno)} [{hostname}]\n{self.format(record)}\n[FAILED REASON: {str(e)}]\n\n")
            except:
                traceback.print_exc(())
            self.handleError(record)

    def emit(self, record):
        if PRODUCTION_MODE:
            if self.threaded:
                t = threading.Thread(target=self.emit_wrapped, args=[record])
                t.start()
            else:
                self.emit_wrapped(record)
        else:
            print(f"Slack logging skipped because server is running in development mode: {record}")
