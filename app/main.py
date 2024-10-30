import json
from fastapi import Depends, FastAPI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

from app.routers import courses
from app.routers import professors
where_am_i = os.environ.get("WHEREAMI", None)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    with open("openapi.json") as f:
        app.openapi_schema = json.load(f)
        return app.openapi_schema

app.openapi = custom_openapi
app.include_router(courses.router)
app.include_router(professors.router)


@app.get('/')
def hello_world():
    global where_am_i

    if where_am_i is None:
        where_am_i = "NOT IN DOCKER"

    return f"Hello, from {where_am_i}! I changed and I'm microservice 3."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



