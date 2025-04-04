from fastapi import APIRouter, Depends
#from app.dependencies.firebase import get_auth

router = APIRouter()
@router.get("/")
def read_root():
    return {
        "Hello": "World"
    }