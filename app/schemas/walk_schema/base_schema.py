from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class Coordinate(BaseModel):
    latitude: float = Field(examples=[127.029230599])
    longitude: float = Field(examples=[37.586331295])

class Image(BaseModel):
    url: HttpUrl
    name: str

class UserWalkSummary(BaseModel):
    walk_distance: float # 사용자가 산책한 총 거리 (km 단위)
    walk_time: int # 사용자가 산책한 총 시간 (분 단위)

    model_config = ConfigDict(from_attributes=True)