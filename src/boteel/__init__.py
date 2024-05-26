
from boteel.database import Database
from boteel.conf import global_settings

db: Database = None

settings: global_settings = None

app_dirs: list = []
app_dict: dict = {}

DEBUG = "text-bg-light"
INFO = "text-bg-primary"
SUCCESS = "text-bg-success"
WARNING = "text-bg-warning"
ERROR = "text-bg-danger"

message_constants = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "SUCCESS": SUCCESS,
    "WARNING": WARNING,
    "ERROR": ERROR,
}
