from bson import ObjectId
from pydantic import BaseModel, Field
from app.schemas.walk_schema.base_schema import Coordinate, Image



class GetRecommendationResDTO(BaseModel):
    location: Coordinate
    start_name: str = Field(..., examples=["고려대학교 애기능생활관"])
    address: str = Field(..., examples=["서울특별시 성북구 고려대로 지하89"])
    distance: float = Field(..., examples=[1.0])
    walks: int = Field(..., examples=[30])
    time: int = Field(..., examples=[30])
    routes : list[Coordinate]

class PostStartWalkResDTO(BaseModel):
    walk_id: str = Field(..., examples=["67f5be826814492ab754e6fe"])

class PostEndWalkResDTO(BaseModel):
    start_name: str
    end_name: str
    distance: float
    time: int
    avg_speed: float