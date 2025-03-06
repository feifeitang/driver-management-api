# Driver Management API

This is a simple FastAPI application that provides CRUD operations for managing drivers using SQLModel. It allows you to create, read, update, and delete driver records, as well as expose a RESTful API.

## Features
- Create, Read, Update, and Delete drivers.
- Uses SQLite as the database.
- API documentation available via Swagger UI at `/docs`.

## Requirements
- Python 3.7+
- FastAPI
- SQLModel (SQLAlchemy)
- SQLite (used for local development)

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

## Running the Application

You can run the FastAPI app using `uvicorn`:

```bash
uvicorn main:app --reload
```

This will start the development server on `http://127.0.0.1:8000`.

### API Documentation

Once the server is running, you can view the Swagger UI at:

```
http://127.0.0.1:8000/docs
```

You can also interact with the API through `http://127.0.0.1:8000/redoc`.