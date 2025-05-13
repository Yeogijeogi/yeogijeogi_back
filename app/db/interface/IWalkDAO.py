from abc import ABC, abstractmethod


class IWalkDAO(ABC):
    @abstractmethod
    async def check_walk_exists(self, walk_id:str) -> bool: pass

    @abstractmethod
    async def post_start_walk(self, uuid, request): pass

    @abstractmethod
    async def get_walk(self, walk_id): pass

    @abstractmethod
    async def get_latest_walk(self, uuid): pass
