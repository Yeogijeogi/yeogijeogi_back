import pytest

from app.core.config import get_settings
from app.db.Database import Database
from app.db.mongodb import MongoDB
from app.dependencies.firebase import get_auth

@pytest.mark.asyncio
async def test_db_connection():
    database: Database = MongoDB()
    await database.connect_database()
    assert await database.check_status()

@pytest.mark.asyncio
async def test_firebase_connection():
    get_auth()
    assert True

@pytest.mark.skip(reason="Not Implemented")
async def test_openai_connection():
    settings = get_settings()
    if not settings.openai_api_key:
        raise Exception("Open Api Key not found in .env")
