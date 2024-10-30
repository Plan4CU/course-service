import random
import pymysql
from .BaseDataService import DataDataService


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    '''
    This function just defines how to create a connection the SQL DB. 
    '''
    def _get_connection(self):
        try:
            connection = pymysql.connect(
                host=self.context["host"],
                port=self.context["port"],
                user=self.context["user"],
                passwd=self.context["password"],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            # print("Connection to Google Cloud MySQL instance succeeded")
            return connection
        except pymysql.MySQLError as e:
            print("Error connecting to Google Cloud MySQL instance:", e)
            return None 

    '''
    Simple databse retrieval function. It serves as a wrapper for the SQL query 
    where we can pass in the variables into the query.
    '''
    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result

    ''' 
    Insert a new professor into the SQL DB and we will construct 
    their primary key given some algoritm
    for now we will just take the first letter of the first and last name 
    appended with a random number. 
    @Returns Professor object with the new data
    TODO: Handle the case where this p_uni already exists (error handling)
    '''
    def insert_data_object(self,
                        database_name: str,
                        collection_name: str,
                        first_name: str,
                        last_name: str):
        """
        See base class for comments.
        """
        p_uni = first_name[0] + last_name[0] + str(random.randint(0, 100))
        connection = None
        result = None

        try:
            
            sql_statement = f"INSERT INTO {database_name}.{collection_name} " + \
                            f"(p_uni, first_name, last_name) VALUES (%s, %s, %s)"
                        
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [p_uni, first_name, last_name])
            # result = cursor.fetchone()
            
            # TODO: check how we can verify users have created 
            
            # call the function to make the query itself 
            result = self.get_data_object(database_name, collection_name, "p_uni", p_uni)
            # print("SQL search result: " , result)
        except Exception as e:
            if connection:
                connection.close()

        return result
    
    '''
    Making a general update function that will take in the primary key 
    of the professor (p_uni) and the column name that you want to update along with
    the new value.
    @returns Professor object with the updated value
    '''
    def update_data_object(self,
                        database_name: str,
                        collection_name: str,
                        p_uni: str,
                        column_name: str,
                        new_value: str):
        """
        See base class for comments.
        """
        connection = None
        result = None

        try:
            
            sql_statement = f"UPDATE {database_name}.{collection_name} " + \
                            f"SET {column_name}=%s WHERE p_uni=%s"
                        
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [new_value, p_uni])
            
            # grab the updated professor, just to make sure the update worked
            result = self.get_data_object(database_name, collection_name, "p_uni", p_uni)
            
        except Exception as e:
            if connection:
                connection.close()

        return result
    
    '''
    Delete a professor from the SQL DB given their primary key (p_uni)
    @returns true or false depending on the number of lines that were 
    deleted by the query. 
    '''
    def delete_data_object(self,
                        database_name: str,
                        collection_name: str,
                        p_uni: str):
        """
        See base class for comments.
        """
        connection = None
        result = None

        try:
            
            sql_statement = f"DELETE FROM {database_name}.{collection_name} " + \
                            f"WHERE p_uni=%s"
                        
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [p_uni])
            affected_rows = cursor.rowcount
            
            # grab the new professor object, this should assign None to results
            # this primary key should be uniquely assigned to a single professor
            result = self.get_data_object(database_name, collection_name, "p_uni", p_uni)
            print("Deleted this many rows: ", affected_rows)
        except Exception as e:
            if connection:
                connection.close()

        return result == None and affected_rows == 1







