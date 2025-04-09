from bson import ObjectId
from pydantic import BaseModel, Field
from app.schemas.walk_schema.base_schema import Coordinate, Image



class GetRecommendationResDTO(BaseModel):
    location: Coordinate
    name: str = Field(..., examples=["안암역"])
    address: str = Field(..., examples=["서울특별시 성북구 고려대로 지하89"])
    distance: float = Field(..., examples=[1.0])

    time: int = Field(..., examples=[30])
    img: Image
    walk_time: int = Field(..., examples=[30])
    view: int | None = Field(default=0, examples=[0])
    difficulty: int | None = Field(default=0, examples=[0])
    rout : list[Coordinate]

class PostStartWalkResDTO(BaseModel):
    walk_id: str = Field(..., examples=["67f5be826814492ab754e6fe"])

class PostEndWalkResDTO(BaseModel):
    start_name: str
    end_name: str
    distance: float
    time: int
    avg_speed: float