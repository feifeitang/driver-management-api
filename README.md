# Driver Management App

This is a FastAPI application following Domain-Driven Design (DDD) principles to manage drivers. The application provides CRUD operations for managing driver records using SQLModel. It allows you to create, read, update, and delete driver records via a RESTful API.

## Features
- Create, Read, Update, and Delete drivers.
- Domain-driven design architecture to separate concerns.
- Uses MySQL as the database.
- API documentation available via Swagger UI at `/docs`.
- Health check API (`/health`) to verify database connection.
- Supports Docker for easy deployment.
- Unit tests to ensure application functionality.

## Architecture
The project is organized into layers, each with its own responsibility:

- **Domain Layer**: Contains the core business logic, including validation rules (e.g., age validation).
- **Service Layer**: Handles business operations and communicates with repositories.
- **Repository Layer**: Manages data persistence and retrieval from the database.
- **API Layer**: Exposes a RESTful interface for interacting with the application.

## Requirements
- Python 3.7+
- FastAPI
- SQLModel (SQLAlchemy)
- MySQL (used for local development)
- pytest (for running unit tests)

## Installation & Deployment
You can choose to run the application **locally** or using **Docker**.

### 1. Running Locally (Manual Installation)

#### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/driver-management-app.git
cd driver-management-app
```

#### 2. Set up a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

#### 3. Install the dependencies:

```bash
pip install -r requirements.txt
```

#### 4. Set up your MySQL database:

Make sure you have a MySQL server running. You'll need to set the environment variable for the database URL:
- Create a `.env` file in the root directory.
- Add the following:

```
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@localhost/<database_name>
```
Replace `<username>`, `<password>`, and `<database_name>` with your actual MySQL credentials.

#### 5. Run the Application

You can run the FastAPI app using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The server will start on:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check API**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

#### 6. Run Unit Tests

To run the unit tests for the application, use `pytest`:

```bash
pytest
```

This will run all the tests in the project and display the results in the terminal.

### 2. Deployment with Docker
If you want to deploy the application in a containerized environment, use **Docker**.

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/driver-management-app.git
cd driver-management-app
```

#### 2. Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build the Docker image
- Start the FastAPI application
- Start a MySQL database container

#### 3. Access the Application

- **Swagger UI**: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)  
- **Health Check API**: [http://0.0.0.0:8000/health](http://0.0.0.0:8000/health)  

#### 4. Stop the Containers

```bash
docker-compose down
```
This will stop and remove all running containers.

## Health Check API
To verify if the database is connected, you can use the `/health` endpoint.

### Checking API Health

```bash
curl -X GET http://0.0.0.0:8000/health
```

#### Database is connected (Healthy)

```json
{
    "status": "ok",
    "message": "Database connection is healthy"
}
```

#### Database is down (Unhealthy)

```json
{
    "detail": "Database connection failed: (error details)"
}
```
