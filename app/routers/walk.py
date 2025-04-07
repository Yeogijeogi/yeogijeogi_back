from fastapi import APIRouter, Depends, Query, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from app.dependencies.firebase import get_auth
from app.dependencies.openai_dependency import get_openai_client
from app.schemas.walk_schema import request_schema, response_schema
from app.dependencies.firebase import get_auth
from app.db.mongodb import MongoUserDatabase, MongoWalkSummaryDatabase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.walk_service import WalkService

security = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials

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
    chain=Depends(get_openai_client),
    token=Depends(get_token),
    auth=Depends(get_auth)
):
    response = await WalkService(token, auth, chain).recommend(latitude=latitude, longitude=longitude, walk_time=walk_time,view=view, difficulty=difficulty)
    return response

@router.post("/start")
async def walk_start(
    request: request_schema.PostStartWalkReqDTO,
    token = Depends(get_token),
    auth=Depends(get_auth)
) -> response_schema.PostStartWalkResDTO:
    response = await WalkService(token = token, auth = auth, chain = None).walk_start(request = request)
    return response_schema.PostStartWalkResDTO(walk_id = response)

@router.post("/location")
async def walk_location(
    request: request_schema.PostLocationReqDTO,
    token = Depends(get_token),
    auth = Depends(get_auth)
):
    response = await WalkService(token=token, auth=auth, chain=None).walk_location(request = request)
    return response
@router.post("/end")
async def post_end()

@router.patch("/end")
async def patch_end