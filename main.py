from fastapi import FastAPI
from games_router import router as games_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Подключаемся к глобальному Redis...")
    yield
    print("🛑 Отключение сервера...")

app = FastAPI(lifespan=lifespan)

app.include_router(games_router)