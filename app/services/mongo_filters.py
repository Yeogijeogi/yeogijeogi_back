from app.db.dao.MongoWalkDAO import MongoWalkDataBase
from fastapi import HTTPException

from app.db.dao.MongoWalkSummaryDAO import MongoWalkSummaryDAO


def check_walk_exists(func):
    async def wrapper(instance, walk_id:str, *args, **kwargs):
        if not await MongoWalkDataBase().check_walk_exists(walk_id):
            raise HTTPException(status_code=404, detail="Walk Don't Exists")
        return await func(instance, walk_id, *args, **kwargs)
    return wrapper

def check_walk_summary_exists(func):
    async def wrapper(instance, walk_id:str, *args, **kwargs):
        if not await MongoWalkSummaryDAO().check_walk_summary_exists(walk_id):
            raise HTTPException(status_code=404, detail="WalkSummary Don't Exists")
        return await func(instance, walk_id, *args, **kwargs)
    return wrapper