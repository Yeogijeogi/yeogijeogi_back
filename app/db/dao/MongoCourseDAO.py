from app.db.interface.ICourseDAO import ICourseDAO
from app.schemas.course_schema.base_schema import CourseInfo
from typing import List
from fastapi import HTTPException
from beanie import BulkWriter
from bson.objectid import ObjectId

from app.db.models.walks import Walks
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary

class MongoCourseDAO(ICourseDAO):
    aggregate_query = [
        {'$lookup': {'from': 'WalkPoints', 'localField': '_id', 'foreignField': 'walk_id.$id', 'as': 'last_point', 'pipeline': [{'$sort': {'_id': -1}}, {'$limit': 1}]}},
        {'$unwind': {'path': '$last_point'}},
        {'$lookup': {'from': 'WalkSummary', 'localField': '_id', 'foreignField': 'walk_id.$id', 'as': 'walk_summary'}},
        {'$unwind': {'path': '$walk_summary'}}]

    async def get_course_list_by_uuid(self, uuid:str) -> List[CourseInfo]:
        course_info_list = (await Walks.find(Walks.user_id.id == uuid).aggregate(
            aggregation_pipeline=self.aggregate_query,
            projection_model=CourseInfo).to_list())
        return course_info_list

    async def get_one_course_by_walk_id(self, uuid:str, walk_id:str) -> CourseInfo:
        if await Walks.find_one(Walks.id == ObjectId(walk_id), Walks.user_id.id != uuid):
            raise HTTPException(status_code=404, detail="walk-not-found")

        return (await Walks.find(Walks.id == ObjectId(walk_id)).aggregate(
            aggregation_pipeline=self.aggregate_query,
            projection_model=CourseInfo).to_list())[0]

    async def delete_course_by_walk_id(self, uuid:str, walk_id:str):
        if await Walks.find_one(Walks.id == ObjectId(walk_id), Walks.user_id.id != uuid):
            raise HTTPException(status_code=404, detail="walk-not-found")

        async with BulkWriter() as bulk_writer:
            await WalkPoints.find(WalkPoints.walk_id.id == ObjectId(walk_id)).delete(bulk_writer=bulk_writer)
        await bulk_writer.commit()

        async with BulkWriter() as bulk_writer:
            await WalkSummary.find(WalkSummary.walk_id.id == ObjectId(walk_id)).delete(bulk_writer=bulk_writer)
        await bulk_writer.commit()

        w = await Walks.get(walk_id)
        await w.delete()
        return True
