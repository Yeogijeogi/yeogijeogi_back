import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
from beanie import init_beanie, Document

from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks

@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def init_db():
    client = AsyncMongoMockClient()
    database = client["test"]
    await init_beanie(database=database, document_models=[Walks, WalkPoints, WalkSummary])
    return database

@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def clean_db(init_db):
    yield
    collection_list = await init_db.list_collection_names()
    for collection in collection_list:
        await init_db[collection].drop()