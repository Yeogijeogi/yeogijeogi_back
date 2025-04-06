from functools import lru_cache
from fastapi import HTTPException

from firebase_admin import initialize_app, credentials, auth
from app.core.config import get_settings
from app.dependencies.Auth import Auth
import requests

import jwt

def check_token(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])

@lru_cache
class FirebaseAuth(Auth):
    def __init__(self):
        super().__init__()
        settings = get_settings()
        self.api_connected = False
        if settings.firebase_auth:
            self.api_connected = True
            cred = credentials.Certificate(settings.firebase_auth)
            initialize_app(cred)

    def verify_token(self, token):
        try:
            return check_token(token)["user_id"]
        except: raise HTTPException(status_code=401, detail="token validation failed")

    def develop_create_token(self, uid):
        return jwt.encode({"user_id": uid}, 'secret', algorithm="HS256")

def get_auth():
    return FirebaseAuth()