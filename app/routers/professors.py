from fastapi import APIRouter, HTTPException, status

# from app.models.course import CourseSection # import the object 
# from app.resources.course_resource import CourseResource # import the DB wrapper for the object 
from app.services.service_factory import ServiceFactory
from app.models.professor import Professor
from app.resources.professor_resource import ProfessorResource

router = APIRouter()

# expecting the user to call the route /professor/pass in the P_UNI
# return: professor object that is connected to the P_UNI search key 
@router.get("/Professor/search/{P_UNI}", tags=["users"])
async def get_professors(P_UNI: str) -> Professor:

    # TODO Do lifecycle management for singleton resource
    
    # make an instance of the class and then run the DB wrapper
    # search query known as get_by_key 
    # res = ServiceFactory.get_service("CourseResource")
    # result = res.get_by_key(course_id)
    # return result
    
    print("User sent P_UNI = ", P_UNI)
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    result = db_wrapper.get_by_key(P_UNI)
    print("result for user =  ", result)
    return result

# Create a new professor, must take in first name, last name and p_uni
# gets generated for them 
@router.post("/Professor/insert/{first_name}&{last_name}", tags=["users"], status_code=status.HTTP_201_CREATED)
async def insert_professor(first_name: str, last_name:str) -> Professor:
    
    # make an instance of the class and then run the DB wrapper
    # search query known as get_by_key 
    print("User sent first_name = ", first_name, " and last_name = ", last_name)
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    result = db_wrapper.insert_by_fields(first_name, last_name)
    print("result for user =  ", result)
    return result

# Update the first name of an existing Professor profile 
@router.patch("/Professor/update/firstname/{p_uni}&{new_first_name}", tags=["users"])
async def update_professor_first_name(p_uni:str, new_first_name: str) -> Professor:
    
    # make an instance of the class and then run the DB wrapper
    # search query known as get_by_key 
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    if db_wrapper.get_by_key(p_uni) == None:
        return None
    else:
        result = db_wrapper.update_by_fields(p_uni, "first_name", new_first_name)
        return result

# Update the last name of an existing Professor profile 
@router.patch("/Professor/update/lastname/{p_uni}&{new_last_name}", tags=["users"])
async def update_professor_last_name(p_uni:str, new_last_name: str) -> Professor:
    
    # make an instance of the class and then run the DB wrapper
    # search query known as get_by_key 
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    if db_wrapper.get_by_key(p_uni) == None:
        return None
    else:
        result = db_wrapper.update_by_fields(p_uni, "last_name", new_last_name)
        return result


# Update the last name of an existing Professor profile 
@router.delete("/Professor/delete/{p_uni}", tags=["users"])
async def delete_professor(p_uni:str) -> bool:
    
    # make an instance of the class and then run the DB wrapper
    # search query known as get_by_key 
    db_wrapper= ServiceFactory.get_service("ProfessorResource")
    if db_wrapper.get_by_key(p_uni) == None:
        print(f"Professor {p_uni} doesn't exist.")
        return None
    else:
        result = db_wrapper.delete_by_key(p_uni)
        return result