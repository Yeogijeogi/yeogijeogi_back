from contextlib import asynccontextmanager
from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info
from beanie import init_beanie
from fastapi import FastAPI

from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary

settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.mongo_database_name]

# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    ping_response = await database.command("ping")

    if int(ping_response["ok"]) != 1:
        # DB 연결 실패
        raise Exception("Problem connecting to database cluster")
    else:
        info("Connected to database")
        await init_beanie(database=database, document_models=[Walks, WalkPoints, WalkSummary]) # ODM Beanie 초기화

    yield
    client.close()

# DI용 getter 함수
def get_db():
    return database