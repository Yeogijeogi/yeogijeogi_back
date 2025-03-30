from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# app 디렉토리 및 .env 파일을 읽어 Settings의 환경변수로 등록
# .env 파일 내부에 필요 환경변수 작성 필요 ( eg. FIREBASE_AUTH = "cred.json" )
class Settings(BaseSettings):
    firebase_auth: str
    mongo_uri: str
    mongo_database_name: str # Mongo 에서 사용하는 database 명
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='allow')

@lru_cache
def get_settings():
    return Settings()

# 사용 가능한 모든 환경 변수 출력
# print(settings.model_dump())

