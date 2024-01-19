from src.config.database.connection import sessionmanager
from src.domain.models import Base
from src.domain.shared import SharedBase


class BaseMigration:

    def __init__(self) -> None:
        self.metadata = Base.metadata
        self.shared_metadata = SharedBase.metadata

        if sessionmanager._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self.engine = sessionmanager._engine.sync_engine

    def create_tables(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self.engine.execution_options(
                schema_translate_map={None: self.shared_metadata.schema}).connect() as conn:

            shared_tables = self.engine.dialect.get_table_names(conn)
            print(shared_tables)
