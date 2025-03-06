from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# the base class
class DriverBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


# the table model
class Driver(DriverBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


# the public data model
class DriverPublic(DriverBase):
    id: int


# the data model to create a driver
class DriverCreate(DriverBase):
    secret_name: str


# the data model to update a driver
class DriverUpdate(DriverBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


# Create an engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create a session dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Create a driver
@app.post("/drivers/", response_model=DriverPublic)
def create_driver(driver: DriverCreate, session: SessionDep):
    db_driver = Driver.model_validate(driver)
    session.add(db_driver)
    session.commit()
    session.refresh(db_driver)
    return db_driver


# Read drivers
@app.get("/drivers/", response_model=list[DriverPublic])
def read_drivers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    drivers = session.exec(select(Driver).offset(offset).limit(limit)).all()
    return drivers


# Read one driver
@app.get("/drivers/{driver_id}", response_model=DriverPublic)
def read_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


# Update a driver
@app.patch("/drivers/{driver_id}", response_model=DriverPublic)
def update_driver(driver_id: int, driver: DriverUpdate, session: SessionDep):
    driver_db = session.get(Driver, driver_id)
    if not driver_db:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver_data = driver.model_dump(exclude_unset=True)
    driver_db.sqlmodel_update(driver_data)
    session.add(driver_db)
    session.commit()
    session.refresh(driver_db)
    return driver_db


# Delete a driver
@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    session.delete(driver)
    session.commit()
    return {"ok": True}
