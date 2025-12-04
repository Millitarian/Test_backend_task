from litestar.plugins.sqlalchemy import base, filters
from litestar.params import Parameter

from src.config.database import db_config
from src.config.logger import get_logger

logger = get_logger()


async def on_startup() -> None:
    async with db_config.get_engine().begin() as conn:
        logger.info("Database connect start")
        await conn.run_sync(base.BigIntAuditBase.metadata.create_all)

async def provide_limit_offset_pagination(
    current_page: int = Parameter(
        ge=1,
        query="currentPage",
        default=1,
        required=False
    ),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False
    ),
) -> filters.LimitOffset:
    return filters.LimitOffset(page_size, page_size * (current_page - 1))