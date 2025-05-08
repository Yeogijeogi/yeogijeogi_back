from fastapi import APIRouter, Depends
from app.schemas.user_schema.response_schema import GetUserResDTO
from app.db.dao.MongoWalkSummaryDAO import MongoWalkSummaryDAO
from app.db.dao.MongoUserDAO import MongoUserDAO
from app.dependencies.auth import get_uuid
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def get_user_service(user_id:str=Depends(get_uuid),):
    return UserService(MongoUserDAO(user_id), MongoWalkSummaryDAO())
@router.post("", status_code=201, responses={
    401: { "description": "Invalid Token"},
    500: { "description": "Internal Server Error"}
})
# 유저 등록
async def create_user(user_service:UserService=Depends(get_user_service)):
    await user_service.create_user()
    return True

@router.get("", responses={
    200: { "model": GetUserResDTO, "description": "User information"},
    401: {"description": "Invalid Token"},
    500: {"description": "Internal Server Error"}
})
# 유저 총 시간 총 거리 반환
async def get_user_info(user_service:UserService=Depends(get_user_service)):
    return await user_service.get_user_info()

@router.delete("")
# 유저 삭제
async def delete_user(user_service:UserService=Depends(get_user_service)):
    await user_service.delete_user()
    return True


