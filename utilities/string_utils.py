import os
import re
from random import getrandbits

from flask import render_template

from bro_utils import config


def render_template_themed(name, **kwargs):
    return render_template(os.path.join(config['template'], name).replace("\\", "/"), **kwargs)


def camelCaseSplit(text):
    """
    This function splits camel case into separate words
    :param text: Input text
    :return: array of words
    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', text)
    return [m.group(0) for m in matches]


def random_string(length=30):
    return '%0x' % getrandbits(length * 4)