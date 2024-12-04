from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String(10), primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)
    credits = Column(Integer, nullable=False)
    school_id = Column(String(4), ForeignKey("schools.school_id"), nullable=False)

    school = relationship("School", back_populates="courses")
    sections = relationship("Section", back_populates="course")
