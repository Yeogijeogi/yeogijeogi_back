from bson import ObjectId
from fastapi import HTTPException

from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks
from app.schemas.walk_schema.base_schema import UserWalkSummary
from app.db.interface.IWalkSummaryDAO import IWalkSummaryDAO


class MongoWalkSummaryDAO(IWalkSummaryDAO):
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
