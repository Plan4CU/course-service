import os
from dotenv import load_dotenv
from framework.services.service_factory import BaseServiceFactory
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService

class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        load_dotenv()

        if service_name == 'CourseResource':
            import app.resources.course_resource as course_resource
            result = course_resource.CourseResource(config=None)

        elif service_name == 'CourseResourceDataService':
            db_user = str(os.getenv("DB_USER"))
            db_password = str(os.getenv("DB_PASSWORD"))
            db_host = str(os.getenv("DB_HOST"))
            db_port = int(os.getenv("DB_PORT", 3307))

            context = dict(user=db_user, password=db_password, host=db_host, port=db_port)
            data_service = MySQLRDBDataService(context=context)
            result = data_service

        else:
            print(f"Warning: Service '{service_name}' not recognized.")
            result = None

        return result