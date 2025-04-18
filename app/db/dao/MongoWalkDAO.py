from datetime import datetime

from fastapi import HTTPException

from app.db.models.users import Users
from app.db.models.walks import Walks

from app.db.interface.IWalkDAO import IWalkDAO


class MongoWalkDataBase(IWalkDAO):
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
