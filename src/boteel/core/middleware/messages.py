import json
from bottle import HTTPResponse

_messages = []


def message(text: str, tag: str):
    _messages.append({"message": text, "tags": tag})


def message_middleware(view):
    def decorator(*args, **kwargs):
        response = view(*args, **kwargs)
        hx_header = json.dumps({"messages": _messages})
        if isinstance(response, HTTPResponse):
            response.headers["HX-Trigger"] = hx_header
        elif len(_messages) > 0:
            response = HTTPResponse(status=204, headers={"HX-Trigger": hx_header})

        _messages.clear()
        return response

    return decorator
