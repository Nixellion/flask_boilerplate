import logging
import json

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


class BroSlackLogHandler(logging.Handler):
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
                 format='[%(asctime)s] [%(name)s] \n```\n%(message)s\n```'):
        logging.Handler.__init__(self)
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.emojis = emojis if emojis is not None else BroSlackLogHandler.EMOJIS
        self.colors = colors if colors is not None else BroSlackLogHandler.COLORS
        self.formatter = logging.Formatter(format)

    def _make_content(self, record):
        attachements = {
            "fallback": self.format(record),
            "title": logging.getLevelName(record.levelno),
            "text": self.format(record),
            "color": self.colors[record.levelno]
        }
        icon_emoji = getattr(record, 'slack_icon', self.emojis[record.levelno])
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

    def emit(self, record):
        try:
            req = Request(self.webhook_url)
            req.add_header('Content-Type', 'application/json')

            content = self._make_content(record)
            urlopen(req, json.dumps(content).encode("utf-8"))
        except:
            self.handleError(record)

