from contextlib import asynccontextmanager
from functools import lru_cache

from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info
from beanie import init_beanie
from beanie.operators import Push
from mongomock_motor import AsyncMongoMockClient
from fastapi import FastAPI, HTTPException
from datetime import datetime

from app.db.Database import Database, IUserDatabase, IWalkSummaryDatabase, IWalkDatabase, IWalkPointDatabase

from app.db.models.users import Users
from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.schemas.user import GetUserResDTO


@lru_cache
class MongoDB(Database):
    def __init__(self):
        settings = get_settings()
        super().__init__()
        if settings.mongo_uri:
            self.client = AsyncIOMotorClient(settings.mongo_uri)
        else:
            self.client = AsyncMongoMockClient()
        self.database = self.client[settings.mongo_database_name]

    async def check_status(self):
        database = self.get_database()
        ping_response = await database.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to MongoDB")
        else:
            await init_beanie(database=database,
                              document_models=[Walks, WalkPoints, WalkSummary, Users])  # ODM Beanie 초기화
            return True

class MongoUserDatabase(IUserDatabase):
    async def create_user(self, uuid):
        try:
            u = await Users(id=uuid).insert()
        except: raise HTTPException(status_code=500, detail="Database Insertion Failed")

    async def delete_user(self, uuid):
        try:
            u = await Users.find_one(Users.id==uuid)
            await u.delete()
        except: raise HTTPException(status_code=500, detail="Database Deletion Failed")

class MongoWalkSummaryDatabase(IWalkSummaryDatabase):
    async def get_total_walk_summary(self, uuid):
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
                    '_id': '$_id',
                    'walk_time': {
                        '$sum': '$summary.time'
                    },
                    'walk_distance': {
                        '$sum': '$summary.distance'
                    }
                }
            }
            ]
        , projection_model=GetUserResDTO).to_list()
        return k

class MongoWalkDataBase(IWalkDatabase):
    async def post_start_walk(self, uuid, request):
        try:
            await Walks(
                    id = uuid,
                    user_id = request.user_id,
                    start_name = request.start_name,
                    end_name = request.end_name,
                    end_address = request.end_address,
                    img_url = request.img_url,
                    created_at = datetime.now()
                ).insert()
        except:
            raise HTTPException(status_code=500, detail="Database Insertion Failed")

    async def get_walk(self, uuid):
        try:
            walk_data = await Walks.find_one(Walks.user_id==uuid)
            return walk_data
        except:
            raise HTTPException(status_code=500, detail="Database Deletion Failed")

    async def patch_walk(self, uuid, request):
        try:
            walk_data = await Walks.find_one(Walks.id == request.walk_id)
            if not walk_data:
                raise HTTPException(status_code=404, detail="Walk data not found")

            walk_data.end_name = request.end_name
            walk_data.end_address = request.end_address
            await walk_data.save()
        except:
            raise HTTPException(status_code=500, detail="Database Connection Failed")

class MongoWalkPointsDataBase(IWalkPointDatabase):
    async def create_walk_point(self, uuid, request):
        try:
            await WalkPoints(
                    id = uuid,
                    walk_id = request.walk_id,
                    location = request.location,
                    created_at = datetime.now()
                ).insert()
        except:
            raise HTTPException(status_code=500, detail="Database Insertion Failed")

    async def post_walk_point(self, uuid, request):
        try:
            walk_data = await WalkPoints.find_one(WalkPoints.walk_id == request.walk_id)
            if not walk_data:
                raise HTTPException(status_code=404, detail="WalkID Not Found")
            await walk_data.update(Push({
                WalkPoints.routes: {"$each": request.locations}
            }))
        except:
            raise HTTPException(status_code=500, detail="Database Insertion Failed")

    async def get_walk_points(self, uuid, walk_id):
        try:
            walk_points_data = await WalkPoints.find_one(WalkPoints.walk_id==walk_id)
            return walk_points_data
        except:
            raise HTTPException(status_code=500, detail="Database Connection Failed")


# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = MongoDB()
    await db.check_status()
    info("Connected to database")
    yield
    db.get_client().close()