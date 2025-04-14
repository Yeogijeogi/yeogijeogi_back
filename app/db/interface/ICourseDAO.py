from abc import ABC, abstractmethod
from app.schemas.course_schema.base_schema import CourseInfo

class ICourseDAO(ABC):
    @abstractmethod
    async def get_course_list_by_uuid(self, uuid:str) -> [CourseInfo]: pass

    @abstractmethod
    async def get_one_course_by_walk_id(self, uuid:str, walk_id:str) -> CourseInfo: pass

    @abstractmethod
    async def delete_course_by_walk_id(self, uuid:str, walk_id:str) -> bool: pass