import os.path

from functools import lru_cache
from fastapi import HTTPException

from firebase_admin import initialize_app, credentials, auth
from app.core.config import get_settings
from app.dependencies.Auth import Auth

import jwt

def check_token(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])

@lru_cache
class FirebaseAuth(Auth):
    def __init__(self):
        super().__init__()
        settings = get_settings()
        if not settings.firebase_auth:
            raise Exception("Firebase Credential Location not found in .env")
        if not os.path.isfile(f"./{settings.firebase_auth}"):
            raise Exception(f"Firebase Credential File not found in /app/{settings.firebase_auth}")
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