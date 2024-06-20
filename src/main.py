from .router import router as trading_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from fastapi import FastAPI

app = FastAPI(
    title='Spimex'
)

app.include_router(
    trading_router,
    prefix="",
    tags=["Trading"]
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
