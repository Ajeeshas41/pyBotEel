from bottle import route, template, jinja2_view, request
import eel

@route('/index')
@jinja2_view('web/templates/index.html')
def index():
    eel.sleep(2.0)
    return

@route('/new')
@jinja2_view('web/templates/new.html')
def new():
    print(request.headers.environ['HTTP_HX_REQUEST'])
    eel.sleep(2.0)
    return {'items': [1,2,3,4,5,6,7,8,9]}

@route('/about')
@jinja2_view('web/templates/about.html')
def about():
    eel.sleep(2.0)
    return 