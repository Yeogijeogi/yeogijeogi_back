from fastapi import Depends, HTTPException, Response
from app.dependencies.openai_dependency import get_openai_client
from app.schemas.walk_schema import request_schema
from app.db.mongodb import MongoWalkDataBase, MongoWalkPointsDataBase

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

    async def post_walk_end(self):
        uuid = self.auth.verify_token(self.token)
        walk_data = await MongoWalkDataBase().get_walk(uuid = uuid)
        walk_point_data = await MongoWalkPointsDataBase().get_walk_points(uuid = uuid, walk_id = walk_data.walk_id)

        return

    async def patch_end(self, request = request_schema.PatchSaveWalkReqDTO):
        uuid = self.auth.verify_token(self.token)
        await MongoWalkDataBase().patch_walk(uuid = uuid, request=request)
        return
