from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

# app 디렉토리 및 .env 파일을 읽어 Settings의 환경변수로 등록
# .env 파일 내부에 필요 환경변수 작성 필요 ( eg. FIREBASE_AUTH = "cred.json" )
class Settings(BaseSettings):
    firebase_auth: Optional[str] = None
    mongo_uri: Optional[str] = None
    mongo_database_name: Optional[str] = "test"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='allow')

@lru_cache
def get_settings():
    return Settings()