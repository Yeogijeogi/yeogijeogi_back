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
            "user_id": self.token.user_id,
            #"start_name": #네이버맵 사용
            "end_name": request.end_name,
            "end_address": request.end_address,
            "img": request.img
        }
        walk_id = await MongoWalkDataBase().post_start_walk(uuid = uuid, request=walk_input)

        walk_point_input = {
            "id": self.token.user_id,
            "walk_id": walk_id,
            "location": request.location,
        }
        await MongoWalkPointsDataBase().create_walk_point(uuid = uuid, request=walk_point_input)

        return walk_id

    async def walk_location(self, request = request_schema.PostLocationReqDTO):
        uuid = self.auth.verify_token(self.token)
        response = await MongoWalkPointsDataBase().post_walk_point(uuid=uuid, request=reqeust)
        return response

    async def post_walk_end(self):
        uuid = self.auth.verify_token(self.token)
        walk_data = await MongoWalkDataBase().get_walk(uuid = uuid)
        walk_point_data = await MongoWalkPointsDataBase().get_walk_points(uuid = uuid, walk_id = walk_data.walk_id)

        return

