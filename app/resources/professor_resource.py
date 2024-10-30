from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.professor import Professor
from app.services.service_factory import ServiceFactory

# DB wrapper 
class ProfessorResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        # this is the DB wrapper for actually getting a pointer to the data
        #service
        self.data_service = ServiceFactory.get_service("ProfessorResourceDataService")
        
        # define the name of the database 
        self.database = "registrar_data" 
        
        # define the name of the collection/ SQL table 
        self.collection = "Professor" 
        
        # define the name of the primary key column 
        self.key_field= "p_uni" 

    '''
    A simple search function that will take in the primary key of the professor
    @returns Professor object with the data. 
    
    TODO: We need to handle cases where the professor doesn't exist 
    '''
    def get_by_key(self, key: str) -> Professor:

        # grab the instance of the data service created during instantiation
        d_service = self.data_service

        # this is constructing the SQL query to grab the item by the key_field
        # parameter and it returns an object of type Professor 
        # where I'm assuming it populates the SQL data into a CourseSection object 
        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        # cast the data returned into a professor object 
        if result:
            result = Professor(**result)
        return result
    
    ''' 
    This just calls the insert function in the data service and then casts the 
    output from this database wrapper to a professor object for JSON purposes.
    @Returns Professor object with the new data
    
    TODO: Handle the case where this p_uni already exists (error handling)
    '''
    def insert_by_fields(self, first_name: str, last_name: str) -> Professor:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.insert_data_object(
            self.database, self.collection, first_name, last_name
        )
        
        # cast the data returned into a professor object 
        result = Professor(**result)
        return result
    
    '''
    This just calls the update function DB wrapper that will construct
    the update query for us. Pass in the name of the column you'd like to update 
    besides the primary key (maybe?) and the new value into the new_value 
    parameter.
    @returns Professor object with the newly updated data. 
    
    # TODO: How do we handle the attempts at changing the p_uni? 
    '''
    def update_by_fields(self, p_uni:str, column_name: str, new_value: str) -> Professor:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.update_data_object(
            self.database, self.collection, p_uni, column_name, new_value
        )
        
        # cast the data returned into a professor object 
        result = Professor(**result)
        return result
    
    '''
    This function just defines how to delete a professor from the SQL DB
    @returns true or false if the deletion was successful
    '''
    def delete_by_key(self, p_uni:str) -> bool:
        
        d_service = self.data_service
        
        # insert the data into the SQL DB 
        result = d_service.delete_data_object(
            self.database, self.collection, p_uni
        )
        
        return result



