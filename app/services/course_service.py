from typing import List, Optional, Type

from sqlalchemy.orm import Session

from app.models.course import Course


class CourseService:
    @staticmethod
    def get_course(db: Session, course_id: str) -> Optional[Course]:
        return db.query(Course).filter(Course.course_id == course_id).first()

    @staticmethod
    def get_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Course]]:
        return db.query(Course).offset(skip).limit(limit).all()

    @staticmethod
    def get_courses_by_school(db: Session, school_id: str, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).filter(Course.school_id == school_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_course(db: Session, course_id: str, course_name: str, credits: int, school_id: str) -> Course:
        db_course = Course(course_id=course_id, course_name=course_name, credits=credits, school_id=school_id)
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course

    @staticmethod
    def update_course(db: Session, course_id: str, course_name: str, credits: int) -> Optional[Course]:
        db_course = CourseService.get_course(db, course_id)
        if db_course:
            db_course.course_name = course_name
            db_course.credits = credits
            db.commit()
            db.refresh(db_course)
        return db_course

    @staticmethod
    def delete_course(db: Session, course_id: str) -> bool:
        db_course = CourseService.get_course(db, course_id)
        if db_course:
            db.delete(db_course)
            db.commit()
            return True
        return False
