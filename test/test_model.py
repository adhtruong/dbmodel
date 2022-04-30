from datetime import date
from typing import Iterator, Optional, Union
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from db_model import PrimaryKey, register
from db_model.core import mapper_registry
from db_model.field import col, mapped_column


@pytest.fixture(name="engine")
def fixture_engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture(name="session")
def fixture_session(engine: Engine) -> Iterator[Session]:
    connection = engine.connect()
    with Session(bind=connection) as session:
        yield session


def test_primary_key() -> None:
    with pytest.raises(ArgumentError):

        @register
        class NoPrimaryKeyModel:
            name: str
            age: Optional[int]

    @register
    class PrimaryKeyModel:
        id: PrimaryKey[UUID]
        name: str
        age: Optional[int]

    @register
    class CompositePrimaryKeyModel:
        id: PrimaryKey[UUID]
        name: PrimaryKey[str]
        age: Optional[int] = mapped_column(is_primary_key=True)


def test_crud_model(engine: Engine, session: Session) -> None:
    @register
    class Model:
        id: PrimaryKey[UUID]
        name: str
        age: Optional[int] = mapped_column(metadata={"hello": "world"})

    assert isinstance(Model.__table__, Table)  # type: ignore[attr-defined]

    mapper_registry.metadata.create_all(engine)

    models = [
        Model(id=uuid4(), name="John", age=None),
        Model(id=uuid4(), name="Paul", age=20),
    ]
    session.add_all(models)

    assert session.query(Model).all() == models
    assert session.query(Model).where(Model.age == None).all() == models[:1]  # noqa: E711
    assert session.query(Model).where(col(Model.age) == 20).all() == models[1:]

    updated_model: Model = session.query(Model).where(Model.age == 20).one()
    updated_model.age = 25
    session.add(updated_model)

    assert session.query(Model).where(Model.age == 25).one() == updated_model


def test_invalid_model() -> None:
    with pytest.raises(RuntimeError, match=r"Unable to map type typing.Union\[str, datetime.date\]"):

        @register
        class UnionType:
            name: Union[str, date]

    with pytest.raises(
        RuntimeError,
        match=r"Unable to process typing.Union\[str, datetime.date, NoneType\]",
    ):

        @register
        class OptionalUnionType:
            name: Union[str, date, None]
