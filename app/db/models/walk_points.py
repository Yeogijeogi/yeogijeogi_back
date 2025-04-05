from beanie import Document, Link, Indexed, BeanieObjectId
from app.db.models.walks import Walks
from pydantic_extra_types.coordinate import Coordinate
from typing import Annotated
from datetime import datetime

# TODO: location validator

'''
WalkPoints 객체 생성 예시
WalkPoints(
    walk_id=Walks 객체 id,
    location=(lat, long),
    created_at=datetime.now()
)

몽고 디비 내부를 보게 된다면 필요할수도 있는 내용
MongoDB에 저장되는 형태
{
    id: ...,
    walk_id: ...,
    location: { # GeoJSON 정의
        type: "Point",
        coordinate: [long, lat] # 여기는 long, lat!
    }
}
'''
class WalkPoints(Document):
    _id: BeanieObjectId # mongodb 기본 id
    walk_id: Link[Walks]
    location: Annotated[Coordinate, Indexed(index_type="2dsphere")] # pydantic_extra_type Coordinate 클래스, Coordinate(lat, long)으로 초기화 가능
    created_at: datetime # 타임스탬프

    # Coordinate 객체를 GeoJSON 형식으로 변환하는 인코더
    class Settings:
        bson_encoders = {
            Coordinate: lambda c: {
                "type": "Point",
                "coordinates": [c.longitude, c.latitude]
            }
        }