from abc import ABC, abstractmethod


class IWalkPointsDAO(ABC):
    @abstractmethod
    async def create_walk_point(self, request): pass

    @abstractmethod
    async def post_walk_point(self, request): pass

    @abstractmethod
    async def get_walk_points(self, walk_id): pass

    @abstractmethod
    async def get_all_points(self, walk_id): pass
