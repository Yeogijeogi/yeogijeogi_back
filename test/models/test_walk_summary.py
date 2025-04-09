import pytest
from app.db.models.walk_summary import WalkSummary
from pydantic import ValidationError
from bson.objectid import ObjectId

def test_create_walk_summary_success(init_db):
    WalkSummary(
        walk_id=ObjectId(),
        distance=0,
        time=0,
        difficulty=0,
        mood=0,
        memo="memo"
    )
    assert True

def test_create_walk_summary_negative_distance(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),

            distance=-1,
            time=0,
            difficulty=0,
            mood=0,
            memo="memo"
        )

def test_create_walk_summary_negative_time(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),
            distance=0,
            time=-1,
            difficulty=0,
            mood=0,
            memo="memo"
        )

def test_create_walk_summary_invalid_min_difficulty(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),
            distance=0,
            time=0,
            difficulty=0,
            mood=-6,
            memo="memo"
        )

def test_create_walk_summary_invalid_max_difficulty(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),
            distance=0,
            time=0,
            difficulty=0,
            mood=6,
            memo="memo"
        )

def test_create_walk_summary_invalid_min_mood(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),
            distance=0,
            time=0,
            difficulty=0,
            mood=-6,
            memo="memo"
        )

def test_create_walk_summary_invalid_max_mood(init_db):
    with pytest.raises(ValidationError):
        WalkSummary(
            walk_id=ObjectId(),
            distance=0,
            time=0,
            difficulty=0,
            mood=6,
            memo="memo"
        )

