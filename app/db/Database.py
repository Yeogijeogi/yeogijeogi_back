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
    def create_user(self, uuid): pass

    @abstractmethod
    def check_status(self): pass
