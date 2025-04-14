from abc import ABC, abstractmethod


class IWalkDAO(ABC):
    @abstractmethod
    async def post_start_walk(self, uuid, request): pass

    @abstractmethod
    async def get_walk(self, walk_id): pass
