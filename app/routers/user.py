from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import GetUserResDTO
from app.dependencies.firebase import get_auth
from app.db.mongodb import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

security = HTTPBearer(auto_error=False)

def check_token_in_header(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials
@router.post("", status_code=201, responses={
    401: { "description": "Invalid Token"},
    500: { "description": "Internal Server Error"}
})
async def create_user(
            auth=Depends(get_auth),
            db=Depends(get_db),
            token = Depends(check_token_in_header),
    ):
    # 유저 등록
    uuid = auth.verify_token(token)
    await db.create_user(uuid)
    return True
@router.get("", responses={
    200: { "model": GetUserResDTO, "description": "User information"},
    401: {"description": "Invalid Token"},
    500: {"description": "Internal Server Error"}
})
def get_user_info(token: str = Depends(check_token_in_header)):
    # 유저 총 시간 총 거리 반환
    return GetUserResDTO(
        walk_distance=100.0,
        walk_time=40
    )

@router.delete("")
def delete_user(credentials: HTTPAuthorizationCredentials = Depends(security),):
    # 유저 삭제
    return {}

@router.get("/token")
def create_token(uid:str):
    auth = get_auth()
    return auth.develop_create_token(uid).decode("utf-8")