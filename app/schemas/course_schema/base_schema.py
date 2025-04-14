from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from bson.objectid import ObjectId
from datetime import datetime
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary

class CourseInfo(BaseModel):
    id: ObjectId = Field(alias="_id")
    start_name: str
    end_name: str
    end_address: str
    img_url: AnyUrl
    created_at: datetime
    last_point: WalkPoints
    walk_summary: WalkSummary

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)