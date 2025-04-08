from contextlib import asynccontextmanager
from functools import lru_cache

from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info
from beanie import init_beanie
from fastapi import FastAPI, HTTPException
from app.db.Database import Database, IUserDatabase, IWalkSummaryDatabase

from app.db.models.users import Users
from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.schemas.user import GetUserResDTO

@lru_cache
class MongoDB(Database):
    async def connect_database(self) -> None:
        settings = get_settings()
        if not settings.mongo_uri:
            raise Exception("Database URI not found on .env")
        self.client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        self.database = self.client[settings.mongo_database_name]
        await init_beanie(database=self.database,
                          document_models=[Walks, WalkPoints, WalkSummary, Users])  # ODM Beanie 초기화

    async def check_status(self) -> bool:
        database = self.get_database()
        ping_response = await database.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to MongoDB")
        else:
            return True

class MongoUserDatabase(IUserDatabase):
    async def create_user(self, uuid:str):
        if await Users.get(uuid):
            raise HTTPException(status_code=500, detail="User already exists")
        await Users(id=uuid).insert()

    async def delete_user(self, uuid):
        if await Users.get(uuid):
            raise HTTPException(status_code=404, detail="User does not exists")
        u = await Users.find_one(Users.id==uuid)
        await u.delete()

class MongoWalkSummaryDatabase(IWalkSummaryDatabase):
    async def get_total_walk_summary(self, uuid:str) -> GetUserResDTO:
        k = await Walks.aggregate(
            [
                {
                    '$match': {
                        'user_id.$id': uuid
                    }
                }, {
                '$lookup': {
                    'from': 'WalkSummary',
                    'localField': '_id',
                    'foreignField': 'walk_id.$id',
                    'as': 'summary'
                }
            }, {
                '$unwind': '$summary'
            }, {
                '$group': {
                    '_id': '$user_id',
                    'walk_time': {
                        '$sum': '$summary.time'
                    },
                    'walk_distance': {
                        '$sum': '$summary.distance'
                    }
                }
            }
        ], projection_model=GetUserResDTO).to_list()
        if not k:
            return GetUserResDTO(walk_time=0, walk_distance=0)
        return k[0]

# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = MongoDB()
    await db.connect_database()
    await db.check_status()
    info("Connected to database")
    yield
    db.get_client().close()