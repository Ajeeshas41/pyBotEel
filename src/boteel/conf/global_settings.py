from typing import Dict, List
from pathlib import Path


BASE_DIR: str = Path(__file__).resolve().parent.parent.parent
APP_TITLE: str = ""
DB_HOST: str = ""

# This will read all the views models and urls in the application
INSTALLED_APPS = ["boteel.default"]

# This is to configure the global template contexts
# You can pass the dotted file path of a function to this list.
# The function should return a 'dict' object
# Keys can be used in the template context to retrive the value
#   eg: dict = {'user': 'TestUser'}
#   inside template you can use{{ user }} to get the value 'TestUser
CONTEXT_DATA = ["boteel.conf.context.default_context"]

DATABASE = {"adaptor": "boteel.database.adaptors.SQLITE3Adaptor", "file": "sqlite3.db"}

STATIC_ROOT = "static"
TEMPLATE_ROOT = "templates"

CREDENTIAL_FILE: str = ""

app_title: str = ""
installed_apps: List[str] = INSTALLED_APPS
middlewares: List[str] = []
context_data: List[str] = CONTEXT_DATA
debug: bool = False
vebrose: bool = False
database: Dict["str", "str"] | None = DATABASE
use_db: bool = True
