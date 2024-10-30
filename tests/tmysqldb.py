from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
import json


def get_db_service():
    context = dict(user="root", password="dbuserdbuser",
                   host="localhost", port=3306)
    
    data_service = MySQLRDBDataService(context=context)
    
    if data_service is None:
        raise Exception("Could not create data service")
    return data_service


def t1():
    data_service = get_db_service()
    result = data_service.get_data_object(
        "registrar_data",
        "Professor",
        key_field="p_uni",
        key_value="bsb2151"
    )
    print("t1 result = \n", json.dumps(result, indent=4, default=str))


if __name__ == '__main__':
    t1()