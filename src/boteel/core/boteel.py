import os
import eel
from importlib import import_module
from bottle import (
    Bottle,
    BaseTemplate,
    debug as _debug,
    static_file,
)

from boteel.conf import global_settings
from boteel.core.utils.module_loading import import_string
from boteel.conf.routes import path
import boteel

# Adding the package folder to the sys.path
# sys.path.append(backend.root_path)

# Global route cache
_routes = {}


def _static(path: str):
    from boteel import settings, app_dict

    if settings.debug:
        for app, folder in app_dict.items():
            _root = os.path.join(settings.BASE_DIR, folder, "static", app)
            if os.path.exists(os.path.join(_root, path)):
                break
    else:
        for app in app_dict.keys():
            _root = os.path.join(settings.BASE_DIR, "static", "static", app)
            if os.path.exists(os.path.join(_root, path)):
                break

    return static_file(path, root=_root)


def configure_app(app: str):
    # Import url_conf from urls.py in each apps added to the INSTALLED_APPS in settings.py
    url_conf = import_string(app + ".urls.url_conf")

    if not isinstance(url_conf, (list, tuple)):
        raise ValueError(
            "%s.url_conf must be a list or tuple of path, but received %s"
            % (app, type(url_conf))
        )

    # Add routes to the global cache
    for url in url_conf:
        _routes[url["path"]] = url


def source_settings():
    settings = global_settings
    try:
        proxy_settings = import_module("settings")
    except ModuleNotFoundError as e:
        raise FileNotFoundError(
            "Please make sure you created a settings.py file in the project root"
        )

    # To access settngs from backend
    base_dir = getattr(proxy_settings, "BASE_DIR", None)
    if base_dir:
        setattr(settings, "BASE_DIR", base_dir)  
    else:
        raise ValueError("You should provide the BASE_DIR Path variable in the settings.py file")  
    
    setattr(settings, "app_title", getattr(proxy_settings, "APP_TITLE", "Default App"))
    setattr(settings, "debug", getattr(proxy_settings, "DEBUG", False))
    setattr(settings, "vebrose", getattr(proxy_settings, "VEBROSE", False))
    setattr(settings, "middlewares", getattr(proxy_settings, "MIDDLEWARES", []))

    settings.use_db = getattr(proxy_settings, "USE_DB", True)
    database = getattr(proxy_settings, "DATABASE", None)
    if database:
        setattr(settings, "database", database)
    elif settings.use_db:
        setattr(settings, "database", settings.DATABASE)

    settings.context_data.extend(getattr(proxy_settings, "CONTEXT_DATA", []))
    settings.installed_apps.extend(getattr(proxy_settings, "INSTALLED_APPS", []))

    app_dirs = []
    app_dict = {}
    # Config template_dirs
    for iapp in settings.installed_apps:
        temp_dir = iapp.replace(".", "/")
        app_dict[iapp.split(".")[-1]] = temp_dir
        app_dirs.append(temp_dir)

    # To access backend.template_dirs
    setattr(boteel, "app_dirs", app_dirs)
    setattr(boteel, "app_dict", app_dict)
    setattr(boteel, "settings", settings)

    return settings


def init():

    # load settings
    settings = source_settings()

    if settings.debug:
        print("Application running on debug mode.")
        _debug(settings.debug)

    # Create a new bottle instane to be used in this application
    app: Bottle = Bottle()

    # Install middlewares to the app
    for middleware_path in settings.middlewares:
        middleware = import_string(middleware_path)
        app.install(middleware)

    # Create the db object
    db = None
    if settings.use_db and settings.database:
        if not "adaptor" in settings.database:
            raise ValueError("Database config should have a adaptor defined")
        adaptor = import_string(settings.database['adaptor'])
        db = adaptor(settings.database)

    if not db:
        print("Application running without a db")

    # To access backend.db
    setattr(boteel, "db", db)

    # Read and configure urls from installed apps
    for iapp in settings.installed_apps:
        configure_app(iapp)

    # Set-up root path for eel and bottle/template
    root_path = settings.BASE_DIR
    eel.root_path = root_path

    # Add Static route for handling the static files
    _routes["/<path:path>"] = path("/<path:path>", view=_static, name="static")

    def url_for(name, *args, **kwargs):
        return app.router.build(name, *args, **kwargs)

    from boteel.core.template import _get_path

    def get_template(template):
        # Return template path to be used inside template
        return _get_path(template)

    # settings['globals'] is used to pass functions to the template
    tpl_functions = {
        "get_template": get_template,
        "url_for": url_for,
    }

    BaseTemplate.settings["globals"] = tpl_functions

    # Run the context functions and load to the Bottle.BaseTemplate.defaults
    from boteel.core.context_processors import context_processor

    context_paths: list = settings.context_data
    if context_paths:
        for cntx_path in context_paths:
            context_processor(cntx_path)

    # Read and set-up application routes
    for _, route in _routes.items():
        app.route(**route)

    # We need delete root and static routes from eel.BOTTLE_ROUTES
    # Otherwise our routes get overridden by eel default routes
    eel.BOTTLE_ROUTES.pop("/")
    eel.BOTTLE_ROUTES.pop("/<path:path>")

    eel.start("", app=app, port=8000)
