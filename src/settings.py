from pathlib import Path

BASE_DIR: str = Path(__file__).resolve().parent
DEBUG = False
VEBROSE = False

INSTALLED_APPS = []
MIDDLEWARES = [
    "boteel.core.middleware.messages.message_middleware",
    "boteel.core.middleware.htmx.htmx_middleware",
]
USE_DB = False
