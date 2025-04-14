from beanie import BulkWriter
from fastapi import HTTPException

from app.db.interface.IUserDAO import IUserDAO
from app.db.models.users import Users
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks


class MongoUserDAO(IUserDAO):
    def __init__(self, user_id: str):
        super().__init__(user_id)

    async def check_user_exists(self) -> bool:
        if await Users.get(self.user_id):
            return True
        return False

    async def create_user(self):
        if await self.check_user_exists():
            raise HTTPException(status_code=500, detail="User already exists")
        await Users(id=self.user_id).insert()

    async def delete_user(self):
        if not await self.check_user_exists():
            raise HTTPException(status_code=500, detail="User does not exist")

        w_list = await Walks.find(Walks.user_id.id == self.user_id).to_list()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                for wp in await WalkPoints.find(WalkPoints.walk_id.id == w.id).to_list():
                    await wp.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                for ws in await WalkSummary.find(WalkSummary.walk_id.id == w.id).to_list():
                    await ws.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                await w.delete(bulk_writer=bulk_writer)
            await bulk_writer.commit()
        u = await Users.get(self.user_id)
        await u.delete()
