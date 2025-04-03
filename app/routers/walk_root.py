from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from app.dependencies.firebase import get_auth
from app.dependencies.openai_dependency import get_openai_client
from app.schemas.walk_schema import request_schema, response_schema

from app.services.walk_service import WalkService
router = APIRouter(
    prefix="/walk",
    tags=["walk"]
)
@router.get("/recommend")
async def chat_openai(
    latitude: float = Query(...),
    longitude: float = Query(...),
    walk_time: int = Query(...),
    view: int = Query(default=0),
    difficulty: int = Query(default=0),
    chain=Depends(get_openai_client)
):
    response = await WalkService(chain).recommend(latitude=latitude, longitude=longitude, walk_time=walk_time,view=view, difficulty=difficulty)
    return response