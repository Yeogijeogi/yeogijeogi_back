from beanie import Document, Link, Indexed
from app.db.models.walks import Walks
from pydantic_extra_types.coordinate import Coordinate
from typing import Annotated

#[주의] Coordinate 객체는 [위도, 경도],  GeoJSON은 [경도, 위도]
# -90 < 위도 < 90
# -180 < 경도 < 180
class WalkPoints(Document):
    walk_id: Link[Walks]
    location: Annotated[Coordinate, Indexed(index_type="2dsphere")]

    class Settings:
        # Coordinate 객체를 GeoJSON 형식으로 변환하는 인코더
        bson_encoders = {
            Coordinate: lambda c: {
                "type": "Point",
                "coordinates": [c.longitude, c.latitude]
            }
        }