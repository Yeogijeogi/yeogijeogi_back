from app.db.interface.IUserDAO import IUserDAO
from app.db.interface.IWalkSummaryDAO import IWalkSummaryDAO
from app.schemas.user_schema.response_schema import GetUserResDTO
from app.dependencies.firebase import get_auth

class UserService:
    def __init__(self,
                 user_database: IUserDAO,
                 walk_summary_database: IWalkSummaryDAO):
        self.user_database = user_database
        self.walk_summary_database = walk_summary_database

    async def create_user(self) -> bool:
        await self.user_database.create_user()
        return True

    async def get_user_info(self) -> GetUserResDTO:
        user_walk_summary = await self.walk_summary_database.get_total_walk_summary(self.user_database.user_id)
        return GetUserResDTO(
            walk_distance=user_walk_summary.walk_distance,
            walk_time=user_walk_summary.walk_time)

    async def delete_user(self) -> bool:
        await self.user_database.delete_user()
        get_auth().delete_firebase_user(self.user_database.user_id)
        return True