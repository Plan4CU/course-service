# Course Microservice

This repository provides access to course information stored in a dedicated MySQL database. The Course microservice allows for handling data related to courses, specifically supporting basic CRUD operations for adding, viewing, updating, and deleting course records. Initially, each course entry includes fields like Course ID, Title, Description, and Instructor. Future sprints may expand this data model to include additional details such as credits, schedule, and prerequisites.

## Overview

We use **FastAPI** as the route handling framework and **MySQL** for the course database. The DB wrapper to connect and query the MySQL database from Python can be found in the `MySQLCourseDataService.py` file. An OpenAPI specification is available once the application is launched, accessible via the `/docs` endpoint.

To launch the microservice, use the command `uvicorn main:app --reload`. The `--reload` flag restarts the server automatically when file changes are detected, which is helpful for development.

## Installation

For local testing, **DataGrip** or any SQL client can be helpful for setting up and visualizing database tables and data. **VS Code** is recommended for developing this microservice.

## Running the Application

1. **Set up a virtual environment**:
   - Create the virtual environment: `python -m venv venv`
   - Activate the environment:
     - On macOS/Linux: `source venv/bin/activate`
     - On Windows: `.\venv\Scripts\activate`

2. **Install dependencies**:
   - Run `pip install -r requirements.txt` to install all necessary Python libraries.

3. **Set Environment Variables**:
   - Populate the following environment variables to configure the database:
     - `DB_USER`: Username for MySQL
     - `DB_PASSWORD`: Password for MySQL
     - `DB_HOST`: Database host URL (use `localhost` for local development)
     - `DB_PORT`: Port number for MySQL, typically `3306`

4. **Run the Application**:
   - Start the FastAPI application with: `uvicorn main:app --reload`

## API Endpoints

- **GET /courses**: Retrieve a list of all courses.
- **GET /courses/{id}**: Retrieve details for a specific course by ID.
- **POST /courses**: Add a new course to the database.
- **PUT /courses/{id}**: Update information for a specific course by ID.
- **DELETE /courses/{id}**: Delete a course from the database by ID.

Visit the `/docs` endpoint once the application is running to view the full OpenAPI documentation and try out the endpoints interactively.
