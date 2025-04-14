from fastapi import APIRouter, Depends
from app.dependencies.auth import get_uuid
from app.schemas.course_schema.request_schema import DeleteCourseReqDTO
from app.services.course_service import CourseService

from app.db.dao.MongoUserDAO import MongoUserDAO
from app.db.dao.MongoCourseDAO import MongoCourseDAO

router = APIRouter(
    prefix="/course",
    tags=["course"],
)

def get_course_service(uuid:str = Depends(get_uuid)):
    return CourseService(MongoCourseDAO(), MongoUserDAO(uuid))

@router.get("")
async def get_all_course_by_uuid(course_service:CourseService = Depends(get_course_service)):
    return await course_service.get_user_courses()

@router.get("/detail")
async def get_course_detail_by_walk_id(
        walk_id:str,
        course_service:CourseService = Depends(get_course_service)):
    return await course_service.get_course_detail(walk_id)

@router.delete("/delete")
async def delete_course_by_walk_id(
        request:DeleteCourseReqDTO,
        course_service:CourseService = Depends(get_course_service)):
    return await course_service.delete_course(request.walk_id)
