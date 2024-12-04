from typing import List, Optional, Type

from sqlalchemy.orm import Session

from app.models.section import Section


class SectionService:
    @staticmethod
    def get_section(db: Session, section_id: int) -> Optional[Section]:
        return db.query(Section).filter(Section.section_id == section_id).first()

    @staticmethod
    def get_sections(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Section]]:
        return db.query(Section).offset(skip).limit(limit).all()

    @staticmethod
    def get_sections_by_course(db: Session, course_id: str, skip: int = 0, limit: int = 100) -> List[Section]:
        return db.query(Section).filter(Section.course_id == course_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_section(db: Session, section_data: dict) -> Section:
        db_section = Section(**section_data)
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section

    @staticmethod
    def update_section(db: Session, section_id: int, section_data: dict) -> Optional[Section]:
        db_section = SectionService.get_section(db, section_id)
        if db_section:
            for key, value in section_data.items():
                setattr(db_section, key, value)
            db.commit()
            db.refresh(db_section)
        return db_section

    @staticmethod
    def delete_section(db: Session, section_id: int) -> bool:
        db_section = SectionService.get_section(db, section_id)
        if db_section:
            db.delete(db_section)
            db.commit()
            return True
        return False
