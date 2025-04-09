import pytest
from datetime import datetime

from app.db.models.walks import Walks

def test_create_walks_success(init_db):
    Walks(
        user_id="some uuid",
        start_name="start name",
        end_name="end name",
        end_address="end address",
        img_url="http://example.com",
        created_at=datetime.now()
    )
    assert True

@pytest.mark.skip(reason="not implemented")
def test_create_walks_invalid_url(init_db):
    pass