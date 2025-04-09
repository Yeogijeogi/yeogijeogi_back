import pytest_asyncio

from app.db.Database import Database
from app.db.mongodb import MongoDB

@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def init_db():
    db: Database = MongoDB()
    await db.connect_database()
    await db.check_status()