from fastapi import FastAPI
from app.routers import root, walk, user, temp, course
from contextlib import asynccontextmanager
from app.db.mongodb import MongoDB
from logging import info
from app.core.config import get_settings
from firebase_admin import initialize_app, credentials, auth, storage
import os

# fastapi lifespan 방식 서버 실행시 초기화 및 종료시 자동 정리
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    settings = get_settings()
    if not settings.firebase_auth:
        raise Exception("Firebase Credential Location not found in .env")
    if not os.path.isfile(f"./{settings.firebase_auth}"):
        raise Exception(f"Fireb\ase Credential File not found in /app/{settings.firebase_auth}")
    cred = credentials.Certificate(settings.firebase_auth)
    initialize_app(cred, {
        "storageBucket": "yeogijeogi-3d5a4.firebasestorage.app"
    })
    info("Connected to Firebase")

    db = MongoDB()
    await db.connect_database()
    await db.check_status()
    info("Connected to database")
    yield
    db.get_client().close()

app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(walk.router)
app.include_router(course.router)
app.include_router(user.router)
app.include_router(temp.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
