from pydantic import BaseModel


class Course(BaseModel):
    course_id: str
    course_name: str
    call_num: int
    professor: str
    credits: int
    is_prereq: bool
    has_prereq: bool
    is_core: bool
    semester: str
    year: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "course_id": "COMS4153W",
                "course_name": "Cloud Computing",
                "call_num": 12345,
                "professor": "dff9",
                "credits": 3,
                "is_prereq": False,
                "has_prereq": True,
                "is_core": False,
                "semester": "FA",
                "year": 2024
            }
        }
