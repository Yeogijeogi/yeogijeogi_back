from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from logging import info

settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_uri)
database = client["test"]



@asynccontextmanager
async def db_lifespan(app: FastAPI):
    ping_response = await database.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster")
    else:
        info("Connected to database")

    yield
    client.close()