from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import storage

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

@router.post("/course_image")
def insert_course_image(walk_id:str, image : UploadFile):
    bucket = storage.bucket()
    blob = bucket.blob(blob_name="images/" + walk_id + ".png")
    blob.upload_from_file(image.file, content_type=image.content_type)
    return True
