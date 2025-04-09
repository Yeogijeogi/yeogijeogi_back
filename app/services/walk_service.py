from fastapi import Depends, HTTPException, Response
from app.dependencies.openai_dependency import get_openai_client
from app.schemas.walk_schema import request_schema, response_schema
from app.db.mongodb import MongoWalkDataBase, MongoWalkPointsDataBase, MongoWalkSummaryDatabase

from math import radians, sin, cos, sqrt, atan2

class WalkService:
    def __init__(self, auth, token, chain) -> None:
        self.chain = chain
        self.token = token
        self.auth = auth

    # 채팅 함수
    async def recommend(self, latitude: float, longitude: float, walk_time: int, view: int, difficulty: int):
        recom_response = await self.chain.ainvoke({
            "latitude": latitude,
            "longitude": longitude,
            "walk_time": walk_time,
            "view": view,
            "difficulty": difficulty
        })
        return recom_response
    
    #산책 시작 서비스
    async def walk_start(self, request = request_schema.PostStartWalkReqDTO):
        uuid = self.auth.verify_token(self.token)
        walk_input = {
            "user_id": uuid,
            "start_name": "hihi",
            "end_name": request.end_name,
            "end_address": request.end_address,
            "img_url": request.img_url
        }
        walk_id = await MongoWalkDataBase().post_start_walk(uuid = uuid, request=walk_input)
        walk_point_input = {
            "walk_id": walk_id,
            "location": request.location,
        }
        await MongoWalkPointsDataBase().create_walk_point(request=walk_point_input)

        return str(walk_id)

    async def walk_location(self, request = request_schema.PostLocationReqDTO):
        uuid = self.auth.verify_token(self.token)
        response = await MongoWalkPointsDataBase().post_walk_point(request=request)
        return response

    async def post_walk_end(self, request):
        uuid = self.auth.verify_token(self.token)
        points = await MongoWalkPointsDataBase().get_all_points(walk_id=request.walk_id)
        len_data = len(points)
        time_diff = points[len_data - 1]["created_at"] - points[0]["created_at"]
        time_diff = time_diff.total_seconds() // 60
        dist = 0

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000  # Earth radius in meters
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        for i in range(len_data - 1):
            lon1, lat1 = points[i]["location"].longitude, points[i]["location"].latitude
            lon2, lat2 = points[i + 1]["location"].longitude, points[i + 1]["location"].latitude
            dist += haversine(lat1, lon1, lat2, lon2)

        start_name, end_name = await MongoWalkSummaryDatabase().create_walk_summary(request, time_diff, dist)

        return response_schema.PostEndWalkResDTO(
            start_name=start_name,
            end_name=end_name,
            distance=dist,
            time=time_diff,
            avg_speed=dist/time_diff if time_diff != 0 else 0
        )


    async def patch_end(self, request = request_schema.PatchSaveWalkReqDTO):
        await MongoWalkSummaryDatabase().patch_walk(request)
        return True
