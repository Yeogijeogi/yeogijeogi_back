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