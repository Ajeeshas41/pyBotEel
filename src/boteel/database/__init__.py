from typing import List
from sqlalchemy import Engine, text
from boteel.core.utils.decorators import log_exception


class Database:
    _engine: Engine = None

    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine: Engine):
        self._engine = engine

    @log_exception
    def get(self, query: str) -> List:
        if not query:
            return []

        data: list = []

        with self._engine.connect() as conn:
            res = conn.execute(text(query))
            for row in res:
                data.append(row._asdict())

        return data

    @log_exception
    def update_data(self, query):
        data: int = 0
        with self._engine.connect() as conn:
            res = conn.execute(text(query))
            data = res.rowcount

        return data
