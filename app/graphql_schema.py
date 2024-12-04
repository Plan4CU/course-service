from typing import List

import strawberry
from strawberry.fastapi import GraphQLRouter

from app.models.course import Course as CourseModel
from app.models.section import Section as SectionModel
from app.utils.database import SessionLocal


@strawberry.type
class Course:
    course_id: str
    course_name: str
    credits: int
    school_id: str


@strawberry.type
class Section:
    section_id: int
    section_num: int
    p_uni: str
    capacity: int
    day: str
    start_time: str
    end_time: str
    semester: str
    year: int
    course_id: str


@strawberry.type
class Query:
    @strawberry.field
    def course(self, course_id: str) -> Course:
        with SessionLocal() as session:
            course = session.query(CourseModel).filter(CourseModel.course_id == course_id).first()
            return Course(
                course_id=course.course_id,
                course_name=course.course_name,
                credits=course.credits,
                school_id=course.school_id
            )

    @strawberry.field
    def courses(self) -> List[Course]:
        with SessionLocal() as session:
            courses = session.query(CourseModel).all()
            return [Course(
                course_id=course.course_id,
                course_name=course.course_name,
                credits=course.credits,
                school_id=course.school_id
            ) for course in courses]

    @strawberry.field
    def section(self, section_id: int) -> Section:
        with SessionLocal() as session:
            section = session.query(SectionModel).filter(SectionModel.section_id == section_id).first()
            return Section(
                section_id=section.section_id,
                section_num=section.section_num,
                p_uni=section.p_uni,
                capacity=section.capacity,
                day=section.day,
                start_time=str(section.start_time),
                end_time=str(section.end_time),
                semester=section.semester,
                year=section.year,
                course_id=section.course_id
            )


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
