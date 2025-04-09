from typing import List
from pydantic import BaseModel

class GeoJson(BaseModel):
    type:str = "Point"
    coordinates:List = [0, 0] # long, lat
