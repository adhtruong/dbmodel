from sqlalchemy import create_engine

from db_model import DBModel, PrimaryKey, get_metadata
from db_model.orm import Session
from db_model.sql import select


class MyModel(DBModel):
    id: PrimaryKey[int]
    name: str


engine = create_engine("sqlite:///:memory:", future=True)

get_metadata().create_all(engine)

with Session(bind=engine) as session:
    session.add(MyModel(id=1, name="John"))
    result = session.execute(select(MyModel))
