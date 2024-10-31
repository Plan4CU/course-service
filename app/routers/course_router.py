from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, status, Query

from app.models.course import Course
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/courses/{course_id}", tags=["courses"], response_model=Course)
async def get_course(course_id: str) -> Course:
    res = ServiceFactory.get_service("CourseResource")
    result = res.get_by_key(course_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {course_id} not found")
    return result


@router.post("/courses", tags=["courses"], response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(course: Course) -> Course:
    res = ServiceFactory.get_service("CourseResource")
    result = res.insert_by_fields(course.dict())
    return result


@router.patch("/courses/{course_id}", tags=["courses"], response_model=Course)
async def update_course(course_id: str, course: Course) -> Course:
    res = ServiceFactory.get_service("CourseResource")
    if res.get_by_key(course_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {course_id} not found")
    result = res.update_by_fields(course_id, course.dict())
    return result


@router.delete("/courses/{course_id}", tags=["courses"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: str):
    res = ServiceFactory.get_service("CourseResource")
    if res.get_by_key(course_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {course_id} not found")
    res.delete_by_key(course_id)
    return None


@router.get("/courses", tags=["courses"], response_model=Dict[str, Any])
async def get_all_courses(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        professor_id: Optional[str] = None
) -> Dict[str, Any]:
    res = ServiceFactory.get_service("CourseResource")
    result = res.get_all_courses(page, size, professor_id)
    return result
