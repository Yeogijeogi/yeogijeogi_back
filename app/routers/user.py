import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks
from app.db.models.users import Users
from app.schemas.user import GetUserResDTO
from app.dependencies.firebase import get_auth
from app.db.mongodb import MongoUserDatabase, MongoWalkSummaryDatabase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

security = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials
@router.post("", status_code=201, responses={
    401: { "description": "Invalid Token"},
    500: { "description": "Internal Server Error"}
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
    200: { "model": GetUserResDTO, "description": "User information"},
    401: {"description": "Invalid Token"},
    500: {"description": "Internal Server Error"}
})
async def get_user_info(token: str = Depends(get_token),
                  auth=Depends(get_auth),
                  walk_summary_database=Depends(MongoWalkSummaryDatabase)):
    # 유저 총 시간 총 거리 반환
    uuid = auth.verify_token(token)
    user_data = await walk_summary_database.get_total_walk_summary(uuid)
    # print(user_data)
    return user_data

@router.delete("")
async def delete_user(token = Depends(get_token),
                      user_database=Depends(MongoUserDatabase),
                      auth=Depends(get_auth)):
    # 유저 삭제
    uuid = auth.verify_token(token)
    await user_database.delete_user(uuid)
    return True


