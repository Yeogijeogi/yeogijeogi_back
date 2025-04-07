import pytest

def test_create_walks_success(init_db, create_walks):
    assert True

@pytest.mark.skip(reason="not implemented")
def test_create_walks_invalid_url(init_db, create_walks):
    pass

@pytest.mark.skip(reason="not implemented")
def test_create_walks_invalid_uuid(init_db):
    pass

@pytest.mark.asyncio(loop_scope="session")
async def test_walk_insertion_to_db(init_db, create_walks, clean_db):
    walk = create_walks
    await walk.insert()
    assert True