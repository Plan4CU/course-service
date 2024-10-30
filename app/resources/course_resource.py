from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.course import CourseSection
from app.services.service_factory import ServiceFactory


class CourseResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("CourseResourceDataService")
        self.database = "registrar_data"
        self.collection = "course"
        self.key_field= "sis_course_id"

    def get_by_key(self, key: str) -> CourseSection:

        d_service = self.data_service

        # this is constructing the SQL query to grab the item by the key_field
        # parameter and it returns an object of type CourseSection 
        # where I'm assuming it populates the SQL data into a CourseSection object 
        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = CourseSection(**result)
        return result
    
    def insert_by_fields(self, course_name: str) -> CourseSection:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.insert_data_object(
            self.database, self.collection, course_name
        )
        
        # cast the data returned into a professor object 
        result = CourseSection(**result)
        return result
    
    def update_by_fields(self, course_id: str) -> CourseSection:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.update_data_object(
            self.database, self.collection, course_id
        )
        
        # cast the data returned into a professor object 
        result = CourseSection(**result)
        return result
    
    def delete_by_key(self, course_id:str) -> bool:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.delete_data_object(
            self.database, self.collection, course_id
        )
        
        return result


