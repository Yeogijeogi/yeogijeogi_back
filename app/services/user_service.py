from app.db.Database import IUserDatabase, IWalkSummaryDatabase
from app.db.models.users import Users
from app.db.models.walk_points import WalkPoints
from app.db.models.walks import Walks
from fastapi import HTTPException
from app.schemas.user import GetUserResDTO
from beanie import DeleteRules, BulkWriter
from app.db.models.walk_summary import WalkSummary

class MongoUserDatabase(IUserDatabase):
    @staticmethod
    async def check_user_exist(uuid:str, raise_error=True) -> bool:
        if await Users.get(uuid):
            return True
        return False

    async def create_user(self, uuid:str):
        if await MongoUserDatabase.check_user_exist(uuid):
            raise HTTPException(status_code=500, detail="User already exists")
        await Users(id=uuid).insert()

    async def delete_user(self, uuid:str):
        if not await MongoUserDatabase.check_user_exist(uuid):
            raise HTTPException(status_code=500, detail="User does not exist")

        w_list = await Walks.find(Walks.user_id.id == uuid).to_list()
        w_id_list = []
        for w in w_list:
            w_id_list.append(w.id)

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
