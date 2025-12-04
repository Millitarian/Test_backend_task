import os
from dotenv import load_dotenv

load_dotenv()

from litestar.stores.redis import RedisStore
from redis.asyncio import Redis

redis_client = Redis(host=os.getenv("RADIS_HOST"), port=int(os.getenv("RADIS_PORT")), db=0)

redis_store = RedisStore(redis=redis_client, namespace="app_cache")