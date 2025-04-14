from fastapi import HTTPException
from app.db.interface.ICourseDAO import ICourseDAO
from app.db.interface.IUserDAO import IUserDAO
from app.schemas.course_schema.response_schema import GetCourseDetailResDTO, GetCourseResDTO
from app.schemas.walk_schema.base_schema import Coordinate
from app.schemas.course_schema.base_schema import CourseInfo


def course_info_to_GetCourseDetailDto(total_walk_info: CourseInfo) -> GetCourseDetailResDTO:
    return GetCourseDetailResDTO(
        img_url=total_walk_info.img_url,
        mood=total_walk_info.walk_summary.mood,
        difficulty=total_walk_info.walk_summary.difficulty,
        memo=total_walk_info.walk_summary.memo
    )

def course_info_to_GetCourseResDto(total_walk_info: CourseInfo) -> GetCourseResDTO:
    return GetCourseResDTO(
        walk_id=str(total_walk_info.id),
        location=Coordinate(
            latitude=total_walk_info.last_point.location.coordinates[1],
            longitude=total_walk_info.last_point.location.coordinates[0]
        ),
        name=total_walk_info.end_name,
        address=total_walk_info.end_address,
        distance=total_walk_info.walk_summary.distance,
        time=total_walk_info.walk_summary.time
    )

class CourseService:
    def __init__(self,
                 course_database: ICourseDAO,
                 user_database: IUserDAO):
        self.user_database = user_database
        self.course_database = course_database

    @staticmethod
    def check_user_exists(method):
        async def wrapper(instance, *args, **kwargs):
            if not await instance.user_database.check_user_exists():
                raise HTTPException(status_code=404, detail="User don't exists")
            return await method(instance, *args, **kwargs)
        return wrapper

    @check_user_exists
    async def get_user_courses(self) -> list[GetCourseResDTO]:
        course_info_list = await self.course_database.get_course_list_by_uuid(self.user_database.user_id)
        return list(map(course_info_to_GetCourseResDto, course_info_list))

    @check_user_exists
    async def get_course_detail(self, walk_id: str) -> GetCourseDetailResDTO:
        course_info = await self.course_database.get_one_course_by_walk_id(self.user_database.user_id, walk_id)
        return course_info_to_GetCourseDetailDto(course_info)

    @check_user_exists
    async def delete_course(self, walk_id: str) -> bool:
        return await self.course_database.delete_course_by_walk_id(self.user_database.user_id, walk_id)

