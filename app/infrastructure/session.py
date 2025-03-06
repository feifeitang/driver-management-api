from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import OperationalError
from typing import Generator
from dotenv import load_dotenv
import os


# Load environment variables from the .env file
load_dotenv()

# Get the database connection URL from environment variable
mysql_url = os.getenv("DATABASE_URL")

# If the DATABASE_URL environment variable is not set, raise an error
if not mysql_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine with the database connection URL
engine = create_engine(mysql_url)


# Create the tables
def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        print(f"Error while creating tables: {e}")


# Create a session dependency
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
