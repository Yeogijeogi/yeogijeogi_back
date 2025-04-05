from app.db.models.walk_points import WalkPoints
import pytest_asyncio
from pydantic_extra_types.coordinate import Coordinate
import pytest
from datetime import datetime


def test_create_walk_points_success(insert_walk):
    walk = insert_walk
    WalkPoints(
        walk_id=walk.id,
        location=Coordinate(0, 0),
        created_at=datetime.now()
    )
    assert True

@pytest.mark.skip(reason="not implemented")
def test_create_walk_points_invalid_coordinates(init_db):
    pass