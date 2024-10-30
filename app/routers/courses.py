from fastapi import APIRouter

from app.models.course import CourseSection
from app.resources.course_resource import CourseResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/courses_sections/{course_id}", tags=["users"])
async def get_courses(course_id: str) -> CourseSection:
     
     print("User sent course_id = ", course_id)

     # TODO Do lifecycle management for singleton resource
     res = ServiceFactory.get_service("CourseResource")
     result = res.get_by_key(course_id)
     return result

@router.patch("/courses_sections/{course_id}", tags=["users"])
async def update_course_name(course_id: str, new_course_name: str) -> CourseSection:
    db_wrapper= ServiceFactory.get_service("CourseResource")
    if db_wrapper.get_by_key(course_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {course_id} not found")
        return
    else:
        result = db_wrapper.update_by_fields(course_id, "course_name", new_course_name)
        return result
     
@router.delete("/courses_sections/{course_id}", tags=["users"])
async def delete_course(course_id: str) -> bool:
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    if db_wrapper.get_by_key(course_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {course_id} not found")
        return None
    else:
        result = db_wrapper.delete_by_key(course_id)
        return result