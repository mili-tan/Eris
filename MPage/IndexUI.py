from pywebio.input import *
from pywebio.output import *

import MContext


def index():
    """Index | Eris"""

    clear()
    put_html(MContext.nav)
    put_html(MContext.card)
