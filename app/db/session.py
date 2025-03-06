from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import OperationalError
from typing import Generator


# Define SQLite database URL
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


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
