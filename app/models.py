from sqlmodel import Field, SQLModel


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
