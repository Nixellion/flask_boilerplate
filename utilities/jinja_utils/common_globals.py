"""
Functions from this module are added to jinja's global variables
"""

from flask import Markup


def alert(text, category="danger"):
    return Markup('<div class="alert alert-{}" role="alert">{}</div>'.format(category, text))


enabled_functions = [
    alert
]