from beanie import Document, Link
from app.db.models.walks import Walks
from pydantic import field_validator, ValidationError
from typing import Union

class WalkSummary(Document):
    walk_id: Link[Walks]
    distance: float # should be positive
    time: int # should be positive
    difficulty: float # should be positive
    mood: float
    memo: str

    @field_validator('distance', 'time', 'difficulty', mode="after")
    @classmethod
    def validate_positive(cls, value: Union[int, float]) -> Union[int, float]:
        if value < 0: raise ValueError("Value must be positive")
        return value