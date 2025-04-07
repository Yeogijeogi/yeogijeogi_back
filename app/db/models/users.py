from beanie import Document, Indexed
from typing import Annotated
from beanie import PydanticObjectId
from pydantic import Field

# TODO : uuid validator

class Users(Document):
    id: str = Field(alias="_id")