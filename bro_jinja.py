from flask import Markup
import traceback


def alert(text, category="danger"):
    return Markup('<div class="alert alert-{}" role="alert">{}</div>'.format(category, text))


def html_line_breaks(text):
    return text.replace("\n", "\n<br>")