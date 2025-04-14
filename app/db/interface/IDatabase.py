from abc import ABC, abstractmethod
from app.core.config import get_settings


class IDatabase(ABC):
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
