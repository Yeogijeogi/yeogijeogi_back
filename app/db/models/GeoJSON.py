from typing import List
from pydantic import BaseModel, field_validator, ConfigDict

class GeoJSON(BaseModel):
    type:str = "Point"
    coordinates:List[float] # long, lat

    model_config = ConfigDict(from_attributes=True)

    @field_validator('coordinates', mode='after')
    @classmethod
    def validate_coordinate(cls, coordinates:List[float]) -> List[float]:
        longitude, latitude = coordinates
        if longitude < -90: raise ValueError("the first element(longitude cannot be smaller than -90")
        if longitude > 90: raise ValueError("the first element(longitude cannot be bigger than 90")
        if latitude < -180: raise ValueError("the second element(longitude cannot be smaller than -180")
        if latitude > 180: raise ValueError("the second element(longitude cannot be bigger than 180")
        return coordinates
