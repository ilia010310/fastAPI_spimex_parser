from contextlib import asynccontextmanager

from api.routers import all_routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация при старте
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # yield используется для разделения инициализации и завершения
    yield
    # Завершение при остановке
    await redis.close()

app = FastAPI(
    title='Spimex',
    lifespan=lifespan
)
for router in all_routers:
    app.include_router(router)

origins = [
    "http://localhost:7112",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)





