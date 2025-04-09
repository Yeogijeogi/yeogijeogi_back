from typing import List
from pydantic import BaseModel
from pydantic import field_validator

class GeoJSON(BaseModel):
    type:str = "Point"
    coordinates:List = [0, 0] # long, lat

    @field_validator('coordinates', mode='after')
    @classmethod
    def validate_coordinate(cls, coordinates:List):
        longitude, latitude = coordinates
        if longitude < -90: raise ValueError("the first element(longitude cannot be smaller than -90")
        if longitude > 90: raise ValueError("the first element(longitude cannot be bigger than 90")
        if latitude < -180: raise ValueError("the second element(longitude cannot be smaller than -180")
        if latitude > 180: raise ValueError("the second element(longitude cannot be bigger than 180")
