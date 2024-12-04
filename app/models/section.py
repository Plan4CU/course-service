from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Section(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    section_num = Column(Integer, nullable=False)
    p_uni = Column(String(7), nullable=False)
    capacity = Column(Integer, nullable=False)
    day = Column(String(15))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    semester = Column(String(2), nullable=False)
    year = Column(Integer, nullable=False)
    course_id = Column(String(10), ForeignKey("courses.course_id"), nullable=False)

    course = relationship("Course", back_populates="sections")
