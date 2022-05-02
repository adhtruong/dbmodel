from datetime import date
from typing import Iterator, Optional, Union
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session

from db_model import Mapped, PrimaryKey, register
from db_model.core import DBModel, mapper_registry
from db_model.field import col, mapped_column


@pytest.fixture(name="engine")
def fixture_engine() -> Engine:
    return create_engine("sqlite:///:memory:", future=True)


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
        age: Mapped[Optional[int]] = mapped_column(is_primary_key=True)


def test_crud_model(engine: Engine, session: Session) -> None:
    class Model(DBModel):
        id: PrimaryKey[UUID]
        name: str
        age: Optional[int] = mapped_column(metadata={"hello": "world"})

    assert isinstance(Model.__table__, Table)

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

    assert session.get(Model, updated_model.id) == updated_model
    assert session.query(Model).where(Model.age == 25).one() == updated_model


def test_foreign_key(engine: Engine, session: Session) -> None:
    class Author(DBModel):
        id: PrimaryKey[UUID]
        name: str
        age: Optional[int]

    class Book(DBModel):
        id: PrimaryKey[UUID]
        name: str
        author_id: UUID = mapped_column(foreign_key=Author.id)

    mapper_registry.metadata.create_all(engine)

    author = Author(id=uuid4(), name="My Author", age=20)
    book = Book(id=uuid4(), name="My Book", author_id=author.id)

    session.add(author)
    session.add(book)

    assert session.execute(
        select(Book, Author).join(Author),
    ).all() == [(book, author)]


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
