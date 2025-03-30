from pydantic import AnyUrl
from beanie import Document
from datetime import datetime

class Walks(Document):
    user_id: str
    start_name: str
    end_name: str
    end_address: str
    img_url: AnyUrl
    created_at: datetime