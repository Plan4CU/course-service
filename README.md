# Course Service API

This API provides endpoints for managing courses and sections in an educational institution.

## API Endpoints

### Courses

- `GET /courses`: Retrieve a list of all courses
- `GET /courses/{course_id}`: Retrieve details of a specific course
- `POST /courses`: Create a new course
- `PUT /courses/{course_id}`: Update an existing course
- `DELETE /courses/{course_id}`: Delete a course

### Sections

- `GET /sections`: Retrieve a list of all sections
- `GET /sections/{section_id}`: Retrieve details of a specific section
- `GET /courses/{course_id}/sections`: Retrieve all sections for a specific course
- `POST /sections`: Create a new section
- `PUT /sections/{section_id}`: Update an existing section
- `DELETE /sections/{section_id}`: Delete a section

### GraphQL

- `POST /graphql`: GraphQL endpoint for querying courses and sections

## REST API Best Practices

This API follows these REST API best practices:

1. Use HTTP methods appropriately:
    - GET for retrieving resources
    - POST for creating new resources
    - PUT for updating existing resources
    - DELETE for removing resources

2. Use plural nouns for resource names (e.g., /courses, /sections)

3. Use nested resources for showing relationships (e.g., /courses/{course_id}/sections)

4. Implement pagination for list endpoints to manage large datasets

5. Use HATEOAS (Hypermedia as the Engine of Application State) to make the API self-discoverable

6. Provide meaningful HTTP status codes (200 for success, 201 for creation, 204 for deletion, 400 for bad requests, 404 for not found, etc.)

7. Version the API (currently v1.0.0)

8. Use JSON for request and response bodies

9. Implement proper error handling and return meaningful error messages

10. Use query parameters for filtering, sorting, and pagination

## Running the API

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your environment variables in a `.env` file
3. Run the API: `uvicorn app.main:app --reload`

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.