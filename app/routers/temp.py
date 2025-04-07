import datetime

from pydantic_extra_types.coordinate import Coordinate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.db.models.walk_points import WalkPoints
from app.dependencies.firebase import get_auth

from app.db.models.users import Users
from app.db.models.walks import Walks
from app.db.models.walk_summary import WalkSummary

security = HTTPBearer()

router = APIRouter(
    prefix="/temp",
    tags=["temp"],
)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials

@router.post("/walks")
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
    w = await Walks.find_one(Walks.user_id.id == u.id)
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

@router.post("/walk_points", description="Only for testing Generates Walk Points with logged in user")
async def create_walk_points(token = Depends(get_token),
                             auth = Depends(get_auth),
                             lat: float = 0,
                             long: float = 0,
                             cnt: int = 1):
    uuid = auth.verify_token(token)
    u = await Users.find_one(Users.id == uuid)
    w = await Walks.find_one(Walks.user_id.id == u.id)

    l = []
    for _ in range(cnt):
        wp = WalkPoints(
            walk_id=w.id,
            location=(lat, long),
            created_at=datetime.datetime.now()
        )
        l.append(wp)
    await WalkPoints.insert_many(l)
    return True

@router.get("/token", description="Only for testing Generates JWT token with uid")
def create_token(uid:str):
    auth = get_auth()
    return auth.develop_create_token(uid)

