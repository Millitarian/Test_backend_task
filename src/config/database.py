import os
from dotenv import load_dotenv

load_dotenv()

from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

class DatabaseConfig():
    host: str = os.getenv("DATABASE_HOST")
    port: str = os.getenv("DATABASE_PORT")
    username: str = os.getenv("DATABASE_USERNAME")
    password: str = os.getenv("DATABASE_PASSWORD")
    database_name: str = os.getenv("DATABESE_NAME")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"


databese_url_config = DatabaseConfig()

db_config = SQLAlchemyAsyncConfig(
    connection_string=databese_url_config.url,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False)
)

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=db_config)