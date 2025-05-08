from beanie import Document, Link
from app.db.models.walks import Walks

# TODO: distance, time, difficulty, mood validator

class WalkSummary(Document):
    walk_id: Link[Walks]
    distance: float
    time: int # 총 산책시간(분)
    difficulty: int | None =  None# -5 ~ 5
    mood: int | None = None # -5 ~ 5
    memo: str | None = None