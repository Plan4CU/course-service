from typing import Dict, Any

from app.models.course import Course
from app.services.service_factory import ServiceFactory
from framework.resources.base_resource import BaseResource


class CourseResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = ServiceFactory.get_service("CourseResourceDataService")
        self.database = "registrar_data"
        self.collection = "course"
        self.key_field = "course_id"

    def get_by_key(self, key: str) -> Course:
        result = self.data_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )
        return Course(**result)

    def insert_by_fields(self, course_data: dict) -> Course:
        result = self.data_service.insert_data_object(
            self.database, self.collection, course_data
        )
        return Course(**result)

    def update_by_fields(self, course_id: str, update_data: dict) -> Course:
        result = self.data_service.update_data_object(
            self.database, self.collection, course_id, update_data
        )
        return Course(**result)

    def delete_by_key(self, course_id: str) -> bool:
        result = self.data_service.delete_data_object(
            self.database, self.collection, course_id
        )
        return result

    def get_all_courses(self, page: int, size: int, professor_id: str = None) -> Dict[str, Any]:
        query_params = {}
        if professor_id:
            query_params["professor"] = professor_id

        results, total = self.data_service.get_data_objects(
            self.database, self.collection, query_params=query_params, page=page, size=size
        )

        courses = [Course(**result) for result in results]
        return {
            "items": courses,
            "total": total,
            "page": page,
            "size": size
        }