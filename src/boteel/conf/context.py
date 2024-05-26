


from bottle import request
from boteel import settings, message_constants
from .functions import current_user

def default_context():
    user = current_user()
    app_title = settings.app_title

    return {
        'user': user,
        'request': request,
        'app_title': app_title,
        'message': message_constants,
    }