from datetime import datetime

from fastapi import HTTPException

from app.db.models.users import Users
from app.db.models.walks import Walks

from app.db.interface.IWalkDAO import IWalkDAO
from bson import ObjectId


class MongoWalkDataBase(IWalkDAO):
    async def check_walk_exists(self, walk_id: str) -> bool:
        if await Walks.get(walk_id):
            return True
        return False

    async def post_start_walk(self, uuid, request):
        try:
            u = await Users.find_one(Users.id == uuid)
            w = Walks(
                user_id = u,
                start_name = request["start_name"],
                end_name = request["end_name"],
                end_address = request["end_address"],
                created_at = datetime.now()
            )
            await w.insert()
            return w.id
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Walk Database Insertion Failed")

    async def get_walk(self, walk_id):
        try:
            walk_data = await Walks.find_one(Walks.id==ObjectId(walk_id))
            return walk_data
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Database Deletion Failed")
