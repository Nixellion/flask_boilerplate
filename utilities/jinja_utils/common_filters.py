"""
Functions from this module are added to jinja's filters
Make sure to add them to enabled_filters list
"""

from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension

from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache

from bs4 import BeautifulSoup


oembed_providers = bootstrap_basic(OEmbedCache())


def html_line_breaks(text):
    return Markup(text.replace("\n", "\n<br>"))


def md(content):
    hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
    extras = ExtraExtension()
    markdown_content = markdown(content, extensions=[hilite, extras]).replace("<img",
                                                                                '<img class="inline_image"')
    oembed_content = parse_html(
        markdown_content,
        oembed_providers,
        urlize_all=True,
        # maxwidth=900
        )

    soup = BeautifulSoup(oembed_content, "html.parser")
    iframes = soup.find_all("iframe")
    if iframes is not None:
        if len(iframes) > 0:
            for iframe in iframes:
                iframe['width'] = "100%"
                iframe['height'] = "520"
                if 'vimeo' in iframe['src']:
                    iframe['src'] = iframe['src'] + "?autoplay=0&loop=1&byline=0&portrait=0"

    html_cont = soup.prettify()
    return Markup(html_cont)


enabled_filters = [
    html_line_breaks,
    md
]