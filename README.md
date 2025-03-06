# Driver Management API

This is a FastAPI application following Domain-Driven Design (DDD) principles to manage drivers. The application provides CRUD operations for managing driver records using SQLModel. It allows you to create, read, update, and delete driver records via a RESTful API.

## Features
- Create, Read, Update, and Delete drivers.
- Domain-driven design architecture to separate concerns.
- Uses MySQL as the database.
- API documentation available via Swagger UI at `/docs`.

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

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/driver-management-api.git
cd driver-management-api
```

### 2. Set up a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

### 3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up your MySQL database:

Make sure you have a MySQL server running. You'll need to set the environment variable for the database URL:
- Create a `.env` file in the root directory.
- Add the following:

```
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@localhost/<database_name>
```
Replace `<username>`, `<password>`, and `<database_name>` with your actual MySQL credentials.

## Running the Application

You can run the FastAPI app using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

This will start the development server on `http://127.0.0.1:8000`.

### API Documentation

Once the server is running, you can view the Swagger UI at:

```
http://127.0.0.1:8000/docs
```

You can also interact with the API through `http://127.0.0.1:8000/redoc`.