import pytest_asyncio
import pytest
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie

from app.db.models.users import Users
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks
from datetime import datetime

@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def init_db():
    client = AsyncMongoMockClient()
    database = client["test"]
    await init_beanie(database=database, document_models=[Walks, WalkPoints, WalkSummary, Users])
    return database

@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def clean_db(init_db):
    yield
    collection_list = await init_db.list_collection_names()
    for collection in collection_list:
        await init_db[collection].drop()

@pytest.fixture(scope="function")
def create_users(init_db):
    u = Users(
        user_id="test_user_id"
    )
    return u

@pytest.fixture(scope="function")
def create_walks(init_db, create_users):
    w = Walks(
        user_id=create_users.id,
        start_name="example_안암역",
        end_name="example_고려대역",
        end_address="example_서울특별시 성북구 종암로 지하1",
        img_url="https://url_to_image.com",
        created_at=datetime.now()
    )
    return w

@pytest_asyncio.fixture(loop_scope="session")
async def insert_walk(init_db, create_walks, clean_db):
    walk = create_walks
    await walk.insert()
    return walk
