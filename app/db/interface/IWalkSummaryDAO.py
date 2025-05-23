from abc import ABC, abstractmethod
from app.schemas.walk_schema.base_schema import UserWalkSummary


class IWalkSummaryDAO(ABC):
    @abstractmethod
    async def check_walk_summary_exists(self, walk_id:str) -> bool: pass

    @abstractmethod
    async def get_total_walk_summary(self, uuid:str) -> UserWalkSummary: pass

    @abstractmethod
    async def create_walk_summary(self, request, time_diff, dist): pass

    @abstractmethod
    async def patch_walk(self, request): pass

    @abstractmethod
    async def check_walk_exists(self, walk_id:str) -> bool: pass
