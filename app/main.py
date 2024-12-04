from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.graphql_schema import graphql_app
from app.routes import course_routes, section_routes
from app.utils.database import engine, Base
from app.utils.logging_middleware import logging_middleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Service API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add logging middleware
app.middleware("http")(logging_middleware)

# Include routers
app.include_router(course_routes.router, tags=["courses"])
app.include_router(section_routes.router, tags=["sections"])
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Welcome to the Course Service API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
