import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.logging_middleware import LoggingMiddleware
from app.routers import course_router

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
app.include_router(course_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
