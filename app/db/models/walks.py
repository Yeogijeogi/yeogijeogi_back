from pydantic import AnyUrl
from beanie import Document, BeanieObjectId, Link
from datetime import datetime
from app.db.models.users import Users

# TODO: created_at validator, string length limit

class Walks(Document):
    _id: BeanieObjectId
    user_id: Link[Users]
    start_name: str # ex. 안암역
    end_name: str # ex. 성북천
    end_address: str # 종료 주소명 ex. 서울 성북구 동선동 2가
    created_at: datetime