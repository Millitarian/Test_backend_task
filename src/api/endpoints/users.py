from datetime import datetime
from litestar import Controller, get, post, patch, delete
from litestar.di import Provide

from src.api.models.user import UserCreate, UserPatch
from src.database.models.user import Users

from msgspec import structs, to_builtins

from litestar.pagination import OffsetPagination
from sqlalchemy.ext.asyncio import AsyncSession

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from src.rabbitmq.producer import publish_user_event, UserEvent

import structlog

from litestar.config.response_cache import ResponseCacheConfig
from litestar.stores.redis import RedisStore


class UsersRepository(SQLAlchemyAsyncRepository[Users]):
    model_type = Users

async def provide_users_repo(db_session: AsyncSession) -> UsersRepository:
    return UsersRepository(session=db_session)


class UsersController(Controller):
    path = "/users"
    dependencies = {"users_repo": Provide(provide_users_repo)}

    @get("/", cache=60)
    async def list_users(
            self,
            users_repo: UsersRepository,
            limit_offset: LimitOffset
    ) -> OffsetPagination[Users]:
        results, total = await users_repo.list_and_count(limit_offset)

        return OffsetPagination[Users](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post("/", cache=60)
    async def create_user(
        self,
        data: UserCreate,
        users_repo: UsersRepository
    ) -> Users:
        user = await users_repo.add(Users(**structs.asdict(data)))
        await users_repo.session.commit()
        event = UserEvent(
            event_type="user.created",
            user_id=user.id,
            trace_id = structlog.contextvars.get_contextvars().get('trace_id')
        )
        await publish_user_event(event)
        return user


    @get("/{user_id:int}", cache=60 )
    async def get_user(
        self,
        user_id: int,
        users_repo: UsersRepository
    ) -> Users:
        user = await users_repo.get(user_id)
        return user


    @patch("/{user_id:int}", cache=60)
    async def update_user(
        self,
        user_id: int,
        data: UserPatch,
        users_repo: UsersRepository
    ) -> Users:
        raw_obj = to_builtins(data)
        raw_obj["id"] = user_id
        user = Users(**raw_obj)

        updated_user = await users_repo.update(user)
        await users_repo.session.commit()
        
        event = UserEvent(
            event_type="user.updated",
            user_id=user.id,
            trace_id = structlog.contextvars.get_contextvars().get('trace_id')
        )
        await publish_user_event(event)
        return updated_user


    @delete("/{user_id:int}", cache=60)
    async def delete_user(
        self,
        user_id: int,
        users_repo: UsersRepository
    ) -> None:
        await users_repo.delete(user_id)
        await users_repo.session.commit()
        event = UserEvent(
            event_type="user.deleted",
            user_id=user_id,
            trace_id = structlog.contextvars.get_contextvars().get('trace_id')
        )
        await publish_user_event(event)