from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import GetUserResDTO
from app.dependencies.firebase import get_auth
from app.db.mongodb import MongoUserDatabase, MongoWalkSummaryDatabase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.dependencies.Auth import Auth

from app.routers.ResponseDescription import ResponseDescription

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

security = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials

def get_uuid(token:str = Depends(get_token),
             auth:Auth = Depends(get_auth)) -> str:
    uuid = auth.verify_token(token)
    return uuid
@router.post("", status_code=201, responses={
    401: ResponseDescription.get_401(),
    500: ResponseDescription.get_500()
})
async def create_user(
            auth=Depends(get_auth),
            user_database=Depends(MongoUserDatabase),
            token=Depends(get_token),
    ):
    # 유저 등록
    uuid = auth.verify_token(token)
    await user_database.create_user(uuid)
    return True

@router.get("", responses={
    200: { "model": GetUserResDTO},
    401: ResponseDescription.get_401(),
    500: ResponseDescription.get_500()})
async def get_user_info(
        uuid:str = Depends(get_uuid),
        walk_summary_database=Depends(MongoWalkSummaryDatabase)):
    # 유저 총 시간 총 거리 반환
    user_data_dto: GetUserResDTO = await walk_summary_database.get_total_walk_summary(uuid)
    return user_data_dto

@router.delete("", responses={
    401: ResponseDescription.get_401(),
    404: ResponseDescription.get_404(),
    500: ResponseDescription.get_500()
})
async def delete_user(uuid:str = Depends(get_uuid),
                      user_database=Depends(MongoUserDatabase)):
    # 유저 삭제
    await user_database.delete_user(uuid)
    return True


