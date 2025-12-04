from litestar import Litestar
from litestar.di import Provide

from src.api.router import router

from src.config.database import sqlalchemy_plugin
from src.database.database import on_startup, provide_limit_offset_pagination

from src.config.logger import get_logger
from src.app.middleware import structlog_middleware_factory

from litestar.plugins.sqlalchemy import SQLAlchemySerializationPlugin

from litestar.middleware import DefineMiddleware

from src.app.lifespan import rabbitmq_lifespan

from src.config.redis import redis_store

def create_app() -> Litestar:
    
    logger = get_logger()
    logger.info("app create")
    
    return Litestar(
        route_handlers=[router],
        on_startup=[on_startup],
        lifespan=[rabbitmq_lifespan],
        plugins=[sqlalchemy_plugin, SQLAlchemySerializationPlugin()],
        dependencies={"limit_offset": Provide(provide_limit_offset_pagination)},
        middleware=[DefineMiddleware(structlog_middleware_factory)],
        stores={"redis_backed_store": redis_store}
    )
