# app/config/external_db_connector.py
"""
Reference pattern for connecting to another team's database, read-only.
Not wired into any active code path — instantiate this when a real
cross-team DB dependency comes up.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class ExternalDBConnector:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session = None

    def connect(self):
        self.engine = create_engine(self.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()
        return self

    def execute(self, query: str, params: dict = None):
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")

        stripped = query.strip().lower()
        if not stripped.startswith("select"):
            raise ValueError("ExternalDBConnector only permits SELECT queries.")

        result = self.session.execute(text(query), params or {})
        return result

    def format_result(self, result):
        return [dict(row._mapping) for row in result]

    def close(self):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        self.session = None
        self.engine = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

'''
with ExternalDBConnector(os.getenv("TEAM_X_DATABASE_URL")) as db:
    result = db.execute("SELECT id, name FROM some_table WHERE id = :id", {"id": "123"})
    rows = db.format_result(result)
'''