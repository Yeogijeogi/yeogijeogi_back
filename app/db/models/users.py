from beanie import Document, Indexed
from typing import Annotated

# TODO : uuid validator

class Users(Document):
    user_id:Annotated[str, Indexed(unique=True)] # firebase uuid