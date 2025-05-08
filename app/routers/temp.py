from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import storage

from app.dependencies.firebase import get_auth

security = HTTPBearer()

router = APIRouter(
    prefix="/temp",
    tags=["temp"],
)

@router.post("/course_image")
def insert_course_image(walk_id:str, image : UploadFile):
    bucket = storage.bucket()
    blob = bucket.blob(blob_name="images/" + walk_id + ".png")
    blob.upload_from_file(image.file, content_type=image.content_type)
    return True
