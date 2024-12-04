from datetime import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_user_with_read_access, get_user_with_write_access
from app.services.section_service import SectionService
from app.utils.database import get_db

router = APIRouter()


class Link(BaseModel):
    href: str
    rel: str


class SectionCreate(BaseModel):
    section_num: int
    p_uni: str
    capacity: int
    day: str
    start_time: time
    end_time: time
    semester: str
    year: int
    course_id: str


class SectionUpdate(BaseModel):
    section_num: int
    p_uni: str
    capacity: int
    day: str
    start_time: time
    end_time: time
    semester: str
    year: int


class SectionResponse(BaseModel):
    section_id: int
    section_num: int
    p_uni: str
    capacity: int
    day: str
    start_time: time
    end_time: time
    semester: str
    year: int
    course_id: str
    links: List[Link] = Field(default_factory=list)

    class Config:
        orm_mode = True


@router.get("/sections/{section_id}", response_model=SectionResponse)
def read_section(section_id: int, request: Request, db: Session = Depends(get_db),
                 _=Depends(get_user_with_read_access)):
    db_section = SectionService.get_section(db, section_id)
    if db_section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    response = SectionResponse.from_orm(db_section)
    response.links = [
        Link(href=f"{request.url}", rel="self"),
        Link(href=f"{request.url_for('read_course', course_id=db_section.course_id)}", rel="course")
    ]
    return response


@router.get("/sections", response_model=List[SectionResponse])
def read_sections(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  _=Depends(get_user_with_read_access)):
    sections = SectionService.get_sections(db, skip=skip, limit=limit)
    for section in sections:
        section.links = [
            Link(href=f"{request.url_for('read_section', section_id=section.section_id)}", rel="self"),
            Link(href=f"{request.url_for('read_course', course_id=section.course_id)}", rel="course")
        ]
    return sections


@router.get("/courses/{course_id}/sections", response_model=List[SectionResponse])
def read_sections_by_course(request: Request, course_id: str, skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db), _=Depends(get_user_with_read_access)):
    sections = SectionService.get_sections_by_course(db, course_id, skip=skip, limit=limit)
    for section in sections:
        section.links = [
            Link(href=f"{request.url_for('read_section', section_id=section.section_id)}", rel="self"),
            Link(href=f"{request.url_for('read_course', course_id=course_id)}", rel="course")
        ]
    return sections


@router.post("/sections", response_model=SectionResponse, status_code=201)
def create_section(section: SectionCreate, request: Request, db: Session = Depends(get_db),
                   _=Depends(get_user_with_write_access)):
    new_section = SectionService.create_section(db, section.dict())
    response = SectionResponse.from_orm(new_section)
    response.links = [
        Link(href=f"{request.url_for('read_section', section_id=new_section.section_id)}", rel="self"),
        Link(href=f"{request.url_for('read_course', course_id=new_section.course_id)}", rel="course")
    ]
    return response


@router.put("/sections/{section_id}", response_model=SectionResponse)
def update_section(section_id: int, section: SectionUpdate, request: Request, db: Session = Depends(get_db),
                   _=Depends(get_user_with_write_access)):
    db_section = SectionService.update_section(db, section_id, section.dict())
    if db_section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    response = SectionResponse.from_orm(db_section)
    response.links = [
        Link(href=f"{request.url}", rel="self"),
        Link(href=f"{request.url_for('read_course', course_id=db_section.course_id)}", rel="course")
    ]
    return response


@router.delete("/sections/{section_id}", status_code=204)
def delete_section(section_id: int, db: Session = Depends(get_db), _=Depends(get_user_with_write_access)):
    success = SectionService.delete_section(db, section_id)
    if not success:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"ok": True}
