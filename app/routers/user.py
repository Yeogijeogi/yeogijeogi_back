import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks
from app.db.models.users import Users
from app.schemas.user import GetUserResDTO
from app.dependencies.firebase import get_auth
from app.db.mongodb import MongoUserDatabase
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
def get_user_info(token: str = Depends(get_token)):
    # 유저 총 시간 총 거리 반환
    return GetUserResDTO(
        walk_distance=100.0,
        walk_time=40
    )

@router.delete("")
async def delete_user(token = Depends(get_token),
                      user_database=Depends(MongoUserDatabase),
                      auth=Depends(get_auth)):
    # 유저 삭제
    uuid = auth.verify_token(token)
    await user_database.delete_user(uuid)
    return True

@router.get("/token", description="Only for testing Generates JWT token with uid")
def create_token(uid:str):
    auth = get_auth()
    return auth.develop_create_token(uid)

@router.post("/walks", description="Only for testing Generates Walks with logged in user")
async def create_walks(token = Depends(get_token),
                 auth=Depends(get_auth)):
    uuid = auth.verify_token(token)
    u = await Users.find_one(Users.id == uuid)
    w = Walks(
        user_id = u,
        start_name="안암역",
        end_name="성북천",
        end_address="서울 성복구 동선동 2가",
        img_url="http://example.com",
        created_at=datetime.datetime.now()
    )
    await w.insert()
    return True

@router.post("/walk_summary", description="Only for testing Generates Walk Summary with logged in user")
async def create_walk_summary(token = Depends(get_token),
                              auth=Depends(get_auth)):
    uuid = auth.verify_token(token)
    u = await Users.find_one(Users.id == uuid)
    w = await Walks.find_one(Walks.user_id.id == uuid)
    ws = WalkSummary(
        walk_id=w.id,
        distance=1231.12312,
        time=10,
        difficulty=-3,
        mood=-3,
        memo="some memo"
    )
    await ws.insert()
    return True