from beanie import Document, Link
from app.db.models.walks import Walks
from datetime import datetime

class WalkSummary(Document):
    walk_id: Link[Walks]
    distance: float
    time: datetime
    difficulty: float
    mood: float
    memo: str