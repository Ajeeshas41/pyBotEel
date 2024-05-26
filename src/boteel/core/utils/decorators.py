import os
from functools import wraps
from bottle import jinja2_view


def template_view(template):
    from eel import root_path

    def decorator(func):
        path = os.path.join(root_path, "templates", template)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return jinja2_view(path)(func)(*args, **kwargs)

        return wrapper

    return decorator


def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except:
            issue = "exception in " + func.__name__ + "\n"
            issue += "-" * 100 + "\n"
            print(issue)
            raise

    return wrapper
