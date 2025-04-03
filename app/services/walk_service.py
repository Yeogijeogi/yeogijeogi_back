from fastapi import Depends, HTTPException, Response
from app.dependencies.openai_dependency import get_openai_client
from app.schemas.walk_schema import request_schema

class WalkService:
    def __init__(self, chain) -> None:
        self.chain = chain

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