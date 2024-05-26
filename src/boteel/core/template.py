import os
from bottle import HTTPResponse, jinja2_template
from boteel import app_dirs, settings


def render(tpl_path, context: dict = None):

    _path = _get_path(tpl_path=tpl_path)
    if not context:
        context = {}
    return HTTPResponse(body=jinja2_template(_path, context))


def _get_path(tpl_path: str):
    _path = None
    if not _path:
        if settings.debug:
            for folder in app_dirs:
                _path = os.path.join(settings.BASE_DIR, folder, "templates", tpl_path)
                if os.path.exists(_path):
                    break
        else:
            for folder in app_dirs:
                _path = os.path.join(settings.BASE_DIR, "static", "templates", tpl_path)
                if os.path.exists(_path):
                    break

    if not _path:
        raise FileNotFoundError("Template '%s', not found." % tpl_path)

    return _path
