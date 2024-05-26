from sqlalchemy import create_engine, URL, Engine
from boteel import settings


class MSSQLAdaptor:
    engine: Engine = None

    def __init__(self, config: dict = None):
        driver = "ODBC Driver 17 for SQL Server"
        if config:
            url = URL.create(
                "mssql+pyodbc",
                host=config["host"],
                database=config["db"],
                query=(["trusted_connection", "yes"], ["driver", driver]),
            )

            self.engine = create_engine(url, echo=settings.vebrose)

class SQLITE3Adaptor:
    engine: Engine = None

    def __init__(self, config: dict = None):
        if config:

            self.engine = create_engine(f"sqlite:///{settings.BASE_DIR / config['file']}", echo=settings.vebrose)