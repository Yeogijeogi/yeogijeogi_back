from pydantic import BaseModel, Field
from app.schemas.walk_schema.base_schema import Coordinate
from fastapi import UploadFile


class PostStartWalkReqDTO(BaseModel):
    start_location: Coordinate
    start_name: str
    end_name: str
    end_address: str

class PostLocationReqDTO(BaseModel):
    walk_id: str
    routes: list[Coordinate]

class PatchSaveWalkReqDTO(BaseModel):
    walk_id: str
    mood: int
    difficulty: int
    memo: str
class PostEndWalkReqDTO(BaseModel):
    walk_id: str