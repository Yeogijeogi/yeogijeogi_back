from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from app.dependencies.firebase import get_auth
from app.dependencies.openai_dependency import get_openai_client
router = APIRouter()
@router.get("/")
def read_root():
    return {
        "Hello": "World"
    }

@router.get("/walk/recommend")
def chat_openai(latitude: float, longitude: float, walk_time: int, view: float, difficulty: float, chain = Depends(get_openai_client)):
    response = chain.invoke({
        "latitude": latitude,
        "longitude": longitude,
        "walk_time": walk_time,
        "view": view,
        "difficulty": difficulty
    })
    return JSONResponse(content=jsonable_encoder(response))