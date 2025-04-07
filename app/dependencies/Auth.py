from abc import ABC, abstractmethod

class Auth(ABC):
    @abstractmethod
    def verify_token(self, token): pass
