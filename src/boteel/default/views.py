

from bottle import HTTPResponse
from boteel.core.template import render


# Default view
def index_view():
    return render('default/index.html')