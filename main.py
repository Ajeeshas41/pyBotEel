
import eel
import route

eel.init('web')

def my_other_thread(text):
    eel.sleep(2.0)         
    eel.js_write(text)


@eel.expose
def print_text(text):
    eel.sleep(2.0)
    print('This is from ' + text)
    eel.spawn(my_other_thread, text)
    return text

eel.start('templates/base.html', jinja_templates='templates')
