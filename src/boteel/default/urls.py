

from boteel.conf.routes import path
from .views import index_view

url_conf = [
    path(route="/", view=index_view)
]