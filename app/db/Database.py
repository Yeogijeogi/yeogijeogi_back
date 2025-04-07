from abc import ABC, abstractmethod
from app.core.config import get_settings
from app.schemas.user import GetUserResDTO


class Database(ABC):
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.database = None

    def get_database(self):
        return self.database

    def get_client(self):
        return self.client

    @abstractmethod
    async def connect_database(self): pass

    @abstractmethod
    async def check_status(self) -> bool: pass

class IUserDatabase(ABC):
    @abstractmethod
    async def create_user(self, uuid:str) -> None: pass

    @abstractmethod
    async def delete_user(self, uuid:str) -> None: pass

class IWalkSummaryDatabase(ABC):
    @abstractmethod
    async def get_total_walk_summary(self, uuid:str) -> GetUserResDTO: pass