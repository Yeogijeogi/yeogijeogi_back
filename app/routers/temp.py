from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies.firebase import get_auth

security = HTTPBearer()

router = APIRouter(
    prefix="/temp",
    tags=["temp"],
)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials

@router.get("/token", description="Only for testing Generates JWT token with uid")
def create_token(uid:str):
    auth = get_auth()
    return auth.develop_create_token(uid)

