from pydantic import AnyUrl, AfterValidator
from beanie import Document
from datetime import datetime
from typing import Annotated
from app.core.config import get_settings

def validate_uuid(token: str) -> str:
    settings = get_settings()
    if settings.firebase_auth:
        # do actual firebase token validation
        return token
    else:
        return token

class Walks(Document):
    user_id: Annotated[str, AfterValidator(validate_uuid)]
    start_name: str
    end_name: str
    end_address: str
    img_url: AnyUrl
    created_at: datetime