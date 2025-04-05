from pydantic import AnyUrl, AfterValidator
from beanie import Document
import datetime
from typing import Annotated
from app.core.config import get_settings

def create_walks(
        user_id = "user_id",
        start_name = "start_name",
        end_name = "end_name",
        end_address = "end_address",
        img_url = "http://example.com",
        created_at = datetime.datetime(2024, 12, 1)):

    return Walks(
        user_id=user_id,
        start_name=start_name,
        end_name=end_name,
        end_address=end_address,
        img_url=img_url,
        created_at=created_at
    )

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
    created_at: datetime.datetime