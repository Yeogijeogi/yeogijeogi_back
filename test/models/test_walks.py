import pytest
from app.db.models.walks import Walks, create_walks
from pydantic import ValidationError

def test_create_walks_success(init_db):
    create_walks()
    assert True

def test_create_walks_invalid_url(init_db):
    with pytest.raises(ValidationError, match="Input should be a valid URL") :
        create_walks(img_url="www.example.com")

@pytest.mark.skip(reason="not implemented")
def test_create_walks_invalid_uuid(init_db):
    pass

@pytest.mark.asyncio(loop_scope="session")
async def test_walk_insertion_to_db(init_db, clean_db):
    walk = create_walks()
    await walk.insert()
    assert await Walks.get(walk.id) == walk