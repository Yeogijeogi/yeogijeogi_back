from app.db.models.users import Users


def test_create_users_success(init_db):
    Users(id="test_uuid")
    assert True