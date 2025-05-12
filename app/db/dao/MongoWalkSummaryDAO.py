from bson import ObjectId
from fastapi import HTTPException

from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks
from app.schemas.walk_schema.base_schema import UserWalkSummary
from app.db.interface.IWalkSummaryDAO import IWalkSummaryDAO


class MongoWalkSummaryDAO(IWalkSummaryDAO):
    async def check_walk_summary_exists(self, walk_id: str) -> bool:
        if await WalkSummary.find_one(WalkSummary.walk_id.id == walk_id):
            return True
        return False

    async def get_total_walk_summary(self, uuid:str) -> UserWalkSummary:
        k = await Walks.aggregate(
            [{
                '$match': {'user_id.$id': uuid}}, {'$lookup': {'from': 'WalkSummary','localField': '_id','foreignField': 'walk_id.$id','as': 'summary'}}, {
                '$unwind': '$summary'}, {
                '$group': {'_id': '$user_id', 'walk_time': {'$sum': '$summary.time'}, 'walk_distance': {'$sum': '$summary.distance'}}}
        ], projection_model=UserWalkSummary).to_list()
        if not k:
            return UserWalkSummary(walk_time=0, walk_distance=0)
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

    async def create_walk_summary(self, walk_id:str, time:int, distance:float):
        w = await Walks.find_one(Walks.id == ObjectId(walk_id))
        ws = WalkSummary(
            walk_id=w,
            time=time,
            difficulty=0,
            mood = 0,
            memo = "",
            distance=distance)
        await ws.insert()

    async def check_walk_exists(self, walk_id: str):
        w = await Walks.find_one(Walks.id == ObjectId(walk_id))

        ws = await WalkSummary.find_one(WalkSummary.walk_id.id == w.id)

        if ws:
            return False
        else:
            return True
