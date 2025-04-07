from pydantic import BaseModel, Field
from app.schemas.walk_schema.base_schema import Coordinate
from fastapi import UploadFile


class PostStartWalkReqDTO(BaseModel):
    location: Coordinate
    end_name: str
    end_address: str
    img: UploadFile | None = None

class PostLocationReqDTO(BaseModel):
    walk_id: str
    routes: list[Coordinate]