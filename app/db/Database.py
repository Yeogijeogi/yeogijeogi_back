from abc import ABC, abstractmethod
from app.core.config import get_settings

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
    async def check_status(self): pass

class IUserDatabase(ABC):
    @abstractmethod
    async def create_user(self, uuid): pass

    @abstractmethod
    async def delete_user(self, uuid): pass

class IWalkSummaryDatabase(ABC):
    @abstractmethod
    async def get_total_walk_summary(self, uuid): pass

    @abstractmethod
    async def create_walk_summary(self, request, time_diff, dist): pass

    @abstractmethod
    async def patch_walk(self, request): pass

class IWalkDatabase(ABC):
    @abstractmethod
    async def post_start_walk(self, uuid, request): pass

    @abstractmethod
    async def get_walk(self, walk_id): pass


class IWalkPointDatabase(ABC):
    @abstractmethod
    async def create_walk_point(self, request): pass

    @abstractmethod
    async def post_walk_point(self, request): pass

    @abstractmethod
    async def get_walk_points(self, walk_id): pass

    @abstractmethod
    async def get_all_points(self, walk_id): pass