from pywebio.input import *
from pywebio.output import *


def index():
    """Index | Eris"""

    clear()
    put_html(open("../nav.html", "r").read())
    put_html(open("../card.html", "r").read())
