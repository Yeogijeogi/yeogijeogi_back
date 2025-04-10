from beanie import Document, Link, Indexed, BeanieObjectId
from app.db.models.walks import Walks
from typing import Annotated
from datetime import datetime
from app.db.models.GeoJSON import GeoJSON

'''
WalkPoints 객체 생성 예시
WalkPoints(
    walk_id=Walks 객체 id,
    location=GeoJson(coordinate=[longitude, latitude]),
    created_at=datetime.now()
)
'''

class WalkPoints(Document):
    _id: BeanieObjectId # mongodb 기본 id
    walk_id: Link[Walks]
    location: Annotated[GeoJSON, Indexed(index_type="2dsphere")]
    created_at: datetime # 타임스탬프