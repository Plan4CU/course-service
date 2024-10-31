import json
from fastapi import FastAPI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from app.routers import course_router
from app.middleware.logging_middleware import LoggingMiddleware

where_am_i = os.environ.get("WHEREAMI", None)

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*']),
    Middleware(LoggingMiddleware)
]

app = FastAPI(middleware=middleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    with open("openapi.json") as f:
        app.openapi_schema = json.load(f)
        return app.openapi_schema

app.openapi = custom_openapi
app.include_router(courses_router.router)

@app.get('/')
def hello_world():
    global where_am_i
    if where_am_i is None:
        where_am_i = "NOT IN DOCKER"
    return f"Hello, from {where_am_i}! I changed and I'm microservice 3."

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)