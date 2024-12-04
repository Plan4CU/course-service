from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.auth.jwt_handler import get_user_with_read_access, get_user_with_write_access
from app.services.course_service import CourseService
from app.utils.database import get_db

router = APIRouter()


class CourseCreate(BaseModel):
    course_id: str
    course_name: str
    credits: int
    school_id: str


class CourseUpdate(BaseModel):
    course_name: str
    credits: int


class Link(BaseModel):
    href: str
    rel: str


class CourseResponse(BaseModel):
    course_id: str
    course_name: str
    credits: int
    school_id: str
    links: List[Link] = Field(default_factory=list)

    class Config:
        orm_mode = True


@router.get("/courses/{course_id}", response_model=CourseResponse)
def read_course(course_id: str, request: Request, db: Session = Depends(get_db),
                _=Depends(get_user_with_read_access)):
    db_course = CourseService.get_course(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    response = CourseResponse.from_orm(db_course)
    response.links = [
        Link(href=f"{request.url}", rel="self"),
        Link(href=f"{request.url_for('read_sections_by_course', course_id=course_id)}", rel="sections"),
        Link(href=f"{request.url_for('read_courses_by_school', school_id=db_course.school_id)}", rel="school_courses")
    ]
    return response


@router.get("/courses", response_model=List[CourseResponse])
def read_courses(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 _=Depends(get_user_with_read_access)):
    courses = CourseService.get_courses(db, skip=skip, limit=limit)
    for course in courses:
        course.links = [
            Link(href=f"{request.url_for('read_course', course_id=course.course_id)}", rel="self"),
            Link(href=f"{request.url_for('read_sections_by_course', course_id=course.course_id)}", rel="sections")
        ]
    return courses


@router.get("/schools/{school_id}/courses", response_model=List[CourseResponse])
def read_courses_by_school(request: Request, school_id: str, skip: int = 0, limit: int = 100,
                           db: Session = Depends(get_db), _=Depends(get_user_with_read_access)):
    courses = CourseService.get_courses_by_school(db, school_id, skip=skip, limit=limit)
    for course in courses:
        course.links = [
            Link(href=f"{request.url_for('read_course', course_id=course.course_id)}", rel="self"),
            Link(href=f"{request.url_for('read_sections_by_course', course_id=course.course_id)}", rel="sections")
        ]
    return courses


@router.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, request: Request, db: Session = Depends(get_db),
                  _=Depends(get_user_with_write_access)):
    new_course = CourseService.create_course(db, **course.dict())
    response = CourseResponse.from_orm(new_course)
    response.links = [
        Link(href=f"{request.url_for('read_course', course_id=new_course.course_id)}", rel="self"),
        Link(href=f"{request.url_for('read_sections_by_course', course_id=new_course.course_id)}", rel="sections")
    ]
    return response


@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: str, course: CourseUpdate, request: Request, db: Session = Depends(get_db),
                  _=Depends(get_user_with_write_access)):
    db_course = CourseService.update_course(db, course_id, **course.dict())
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    response = CourseResponse.from_orm(db_course)
    response.links = [
        Link(href=f"{request.url}", rel="self"),
        Link(href=f"{request.url_for('read_sections_by_course', course_id=course_id)}", rel="sections")
    ]
    return response


@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: str, db: Session = Depends(get_db), _=Depends(get_user_with_write_access)):
    success = CourseService.delete_course(db, course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"ok": True}
