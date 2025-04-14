from pydantic import BaseModel, AnyUrl

from app.schemas.walk_schema.base_schema import Coordinate

class GetCourseResDTO(BaseModel):
    walk_id: str
    location: Coordinate
    name: str
    address: str
    distance: float
    time: int

class GetCourseDetailResDTO(BaseModel):
    img_url: AnyUrl
    mood: int
    difficulty: int
    memo:str