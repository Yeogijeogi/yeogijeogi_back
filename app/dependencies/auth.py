from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from app.dependencies.firebase import get_auth, FirebaseAuth

security = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials: raise HTTPException(status_code=401, detail="Token is Wrong")
    return credentials.credentials

def get_uuid(token:str = Depends(get_token),
             auth = Depends(get_auth)):
    return auth.verify_token(token)
