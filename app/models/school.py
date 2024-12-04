from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


class School(Base):
    __tablename__ = "schools"

    school_id = Column(String(4), primary_key=True, index=True)
    school_name = Column(String(255), nullable=False)

    majors = relationship("Major", back_populates="school")
    courses = relationship("Course", back_populates="school")
