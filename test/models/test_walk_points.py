from app.db.models.walk_points import WalkPoints
from app.db.models.GeoJSON import GeoJSON
import pytest
from datetime import datetime
from pydantic import ValidationError
from bson.objectid import ObjectId

def test_create_walk_points_success(init_db):
    WalkPoints(
        walk_id=ObjectId(),
        location=GeoJSON(coordinates=[0, 0]),
        created_at=datetime.now()
    )
    assert True

def test_create_geo_json_success():
    GeoJSON(coordinates=[0, 0])
    assert True

def test_create_geo_json_invalid_coordinate_min_lat():
    with pytest.raises(ValidationError):
        GeoJSON(coordinates=[0, -181])

def test_create_geo_json_invalid_coordinate_max_lat():
    with pytest.raises(ValidationError):
        GeoJSON(coordinates=[0, 181])

def test_create_geo_json_invalid_coordinate_min_long():
    with pytest.raises(ValidationError):
        GeoJSON(coordinates=[-91, 0])

def test_create_geo_json_invalid_coordinate_max_long():
    with pytest.raises(ValidationError):
        GeoJSON(coordinates=[91, 0])
