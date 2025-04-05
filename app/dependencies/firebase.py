from firebase_admin import initialize_app, credentials, auth
from app.core.config import get_settings

# Firebase Python SDK 연결
cred = credentials.Certificate(get_settings().firebase_auth)
default_app = initialize_app(credential=cred)

def get_auth():
    return auth