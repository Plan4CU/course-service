from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Major(Base):
    __tablename__ = "majors"

    major_id = Column(String(4), primary_key=True, index=True)
    major_name = Column(String(255), nullable=False)
    school_id = Column(String(4), ForeignKey("schools.school_id"), nullable=False)

    school = relationship("School", back_populates="majors")
