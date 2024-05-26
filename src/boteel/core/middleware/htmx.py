from bottle import request

def htmx_middleware(view):

    def decorator(*args, **kwargs):
        is_htmx = request.headers.environ.get("HTTP_HX_REQUEST", False)
        setattr(request, 'htmx', is_htmx)
        return view(*args, **kwargs)

    return decorator