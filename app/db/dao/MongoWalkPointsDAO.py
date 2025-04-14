from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException

from app.db.models.GeoJSON import GeoJSON
from app.db.models.walk_points import WalkPoints
from app.db.models.walks import Walks

from app.db.interface.IWalkPointsDAO import IWalkPointsDAO


class MongoWalkPointsDataBase(IWalkPointsDAO):
    async def create_walk_point(self, request):
        try:
            w = await Walks.find_one(Walks.id == request["walk_id"])
            wp = WalkPoints(
                walk_id=w.id,
                location=GeoJSON(coordinates=[request["location"].longitude, request["location"].latitude]),
                created_at=datetime.now()
            )
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
                    location=GeoJSON(coordinates=[data.longitude, data.latitude]),
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
