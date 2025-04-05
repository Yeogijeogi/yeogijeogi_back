from app.db.models.walk_points import WalkPoints
from app.db.models.walks import create_walks
import pytest_asyncio
from pydantic_extra_types.coordinate import Coordinate

@pytest_asyncio.fixture(loop_scope="session")
async def init_walks(init_db):
    temp_walk = create_walks()
    await temp_walk.insert()
    return temp_walk

def test_create_walk_points_success(init_walks, clean_db):
    temp_walk = init_walks
    WalkPoints(
        walk_id=temp_walk.id,
        location=Coordinate(0, 0)
    )
    assert True

def test_create_walk_points_invalid_coordinates(init_db):
    pass