from pydantic import BaseModel, Field, HttpUrl

class Coordinate(BaseModel):
    latitude: float = Field(examples=[127.029230599])
    longitude: float = Field(examples=[37.586331295])

class Image(BaseModel):
    url: HttpUrl
    name: str