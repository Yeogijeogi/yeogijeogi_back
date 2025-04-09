from contextlib import asynccontextmanager
from functools import lru_cache

from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info
from beanie import init_beanie
from fastapi import FastAPI, HTTPException

from app.db.models.users import Users
from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.db.models.GeoJson import GeoJson
from app.schemas.user import GetUserResDTO

from beanie import BulkWriter
from bson.objectid import ObjectId
from app.db.Database import Database, IWalkPointDatabase, IWalkSummaryDatabase, IUserDatabase, IWalkDatabase
from datetime import datetime

class MongoUserDatabase(IUserDatabase):
    @staticmethod
    async def check_user_exist(uuid:str, raise_error=True) -> bool:
        if await Users.get(uuid):
            return True
        return False

    async def create_user(self, uuid:str):
        if await MongoUserDatabase.check_user_exist(uuid):
            raise HTTPException(status_code=500, detail="User already exists")
        await Users(id=uuid).insert()

    async def delete_user(self, uuid:str):
        if not await MongoUserDatabase.check_user_exist(uuid):
            raise HTTPException(status_code=500, detail="User does not exist")

        w_list = await Walks.find(Walks.user_id.id == uuid).to_list()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                for wp in await WalkPoints.find(WalkPoints.walk_id.id == w.id).to_list():
                    await wp.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                for ws in await WalkSummary.find(WalkSummary.walk_id.id == w.id).to_list():
                    await ws.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                await w.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()
        u = await Users.get(uuid)
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

    async def patch_walk(self, request):
        try:
            w = await Walks.find_one(Walks.id == ObjectId(request.walk_id))
            ws = await WalkSummary.find_one(WalkSummary.walk_id.id == w.id)
            ws.mood = request.mood
            ws.difficulty = request.difficulty
            ws.memo = request.memo
            await ws.save()
            return True

        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Database Connection Failed")

    async def create_walk_summary(self, request, time_diff, dist):
        try:
            w = await Walks.find_one(Walks.id == ObjectId(request.walk_id))
            ws = WalkSummary(
                walk_id=w.id,
                mood = 0,
                difficulty=0,
                memo = "",
                time=time_diff,
                distance=dist
            )
            await ws.insert()
            return w.start_name, w.end_name
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Database Connection Failed")

class MongoWalkDataBase(IWalkDatabase):
    async def post_start_walk(self, uuid, request):
        try:
            u = await Users.find_one(Users.id == uuid)
            w = Walks(
                user_id = u,
                start_name = request["start_name"],
                end_name = request["end_name"],
                end_address = request["end_address"],
                img_url = request["img_url"],
                created_at = datetime.now()
            )
            await w.insert()
            return w.id
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Walk Database Insertion Failed")

    async def get_walk(self, walk_id):
        try:
            walk_data = await Walks.find_one(Walks.id==walk_id)
            return walk_data
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Database Deletion Failed")

class MongoWalkPointsDataBase(IWalkPointDatabase):
    async def create_walk_point(self, request):
        try:
            w = await Walks.find_one(Walks.id == request["walk_id"])
            wp = WalkPoints(
                walk_id=w.id,
                location=GeoJson(coordinates=[request["location"].longitude, request["location"].latitude]),
                created_at=datetime.now()
            )
            print(wp.model_dump())
            l = [wp]
            await WalkPoints.insert_many(l)
            return True
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="WalkPoint Database Insertion Failed")

    async def post_walk_point(self, request):
        try:
            w = await Walks.find_one(Walks.id == ObjectId(request.walk_id))
            l = []
            for data in request.routes:
                wp = WalkPoints(
                    walk_id=w.id,
                    location=GeoJson(coordinates=[data.longitude, data.latitude]),
                    created_at=datetime.now()
                )
                l.append(wp)
            await WalkPoints.insert_many(l)
            return True
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="WalkPoint Database Insertion Failed")
    async def get_walk_points(self, walk_id):
        try:
            walk_points_data = await WalkPoints.find_one(WalkPoints.walk_id==walk_id)
            return walk_points_data
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Database Connection Failed")

    async def get_all_points(self, walk_id):
        try:
            walk_point_data_raw = await WalkPoints.get_motor_collection().find({
                "walk_id.$id": ObjectId(walk_id)
            }).sort("created_at").to_list(length=None)

            walk_point_data = []
            for data in walk_point_data_raw:
                coordinates = data["location"]["coordinates"]
                data["location"] = coordinates # Coordinate(latitude=coordinates[1], longitude=coordinates[0])
                walk_point_data.append(data)
            return walk_point_data

        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="WalkPoint Database Insertion Failed")

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


# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = MongoDB()
    await db.connect_database()
    await db.check_status()
    info("Connected to database")
    yield
    db.get_client().close()