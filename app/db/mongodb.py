from contextlib import asynccontextmanager
from functools import lru_cache

from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from fastapi import FastAPI, HTTPException
from app.db.Database import Database

from app.db.models.users import Users
from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary

@lru_cache
class MongoDB(Database):
    def __init__(self):
        settings = get_settings()
        super().__init__()
        # self.client = AsyncIOMotorClient(settings.mongo_uri)
        self.client = AsyncMongoMockClient()
        self.database = self.client[settings.mongo_database_name]

    async def create_user(self, uuid):
        try:
            u = await Users(user_id=uuid).insert()
        except: raise HTTPException(status_code=500, detail="Database Insertion Failed")

    async def delete_user(self, uuid):
        try:
            u = await Users.find_one(user_id=uuid)
            await u.delete()
        except: raise HTTPException(status_code=500, detail="Database Deletion Failed")

    async def check_status(self):
        database = self.database
        ping_response = await database.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to MongoDB")
        else:
            await init_beanie(database=self.database,
                              document_models=[Walks, WalkPoints, WalkSummary, Users])  # ODM Beanie 초기화
            return True

# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = MongoDB()
    await db.check_status()
    info("Connected to database")
    yield
    db.get_client().close()

# DI용 getter 함수
def get_db():
    return MongoDB()