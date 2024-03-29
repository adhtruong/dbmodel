import json
from datetime import date
from typing import List, Optional, Union
from uuid import UUID, uuid4

import pydantic
import pytest
from sqlalchemy import ForeignKeyConstraint, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError, IntegrityError

from db_model import (
    DBModel,
    Mapped,
    PrimaryKey,
    col,
    get_metadata,
    mapped_column,
    register,
)
from db_model.orm import Session
from db_model.sql import select

metadata = get_metadata()


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

    metadata.create_all(engine)

    models = [
        Model(id=uuid4(), name="John", age=None),
        Model(id=uuid4(), name="Paul", age=20),
    ]
    session.add_all(models)

    assert session.scalars(select(Model)).all() == models
    assert (
        session.execute(select(Model).where(col(Model.age) == None))  # noqa: E711
        .scalars()
        .all()
        == models[:1]
    )
    assert (
        session.execute(select(Model).where(Model.age == 20)).scalars().all()
        == models[1:]
    )

    updated_model = (
        session.execute(select(Model).filter(Model.age == 20)).scalars().one()
    )
    updated_model.age = 25
    session.add(updated_model)

    assert session.get(Model, updated_model.id) == updated_model
    assert session.execute(select(Model).where(Model.age == 20)).all() == []
    assert set(session.execute(select(col(Model.id))).all()) == {
        (model.id,) for model in models
    }


def test_foreign_key(engine: Engine, session: Session) -> None:
    class Author(DBModel):
        id: PrimaryKey[int]
        name: str
        age: Optional[int]

    class Book(DBModel):
        id: PrimaryKey[int]
        name: str
        author_id: int = mapped_column(foreign_key=Author.id)

    metadata.create_all(engine)

    author = Author(id=1, name="My Author", age=20)
    book = Book(id=1, name="My Book", author_id=author.id)
    other_author = Author(id=2, name="Other Author", age=20)

    session.add_all((author, book, other_author))

    assert session.execute(
        select(Book, Author).join(Author),
    ).all() == [(book, author)]
    assert session.execute(
        select(Author, Book).outerjoin(Book).order_by(Author.id),
    ).all() == [(author, book), (other_author, None)]


def test_composite_foreign_key(engine: Engine, session: Session) -> None:
    class Author(DBModel):
        first_name: PrimaryKey[str]
        last_name: PrimaryKey[str]
        age: Optional[int]

    class Book(DBModel):
        name: PrimaryKey[str]
        author_first_name: str
        author_last_name: str

        __table_args__ = (
            ForeignKeyConstraint(
                ("author_first_name", "author_last_name"),
                (Author.first_name, Author.last_name),
            ),
        )

    metadata.create_all(engine)

    author = Author(first_name="John", last_name="Smith", age=20)
    book = Book(name="My Book", author_first_name="John", author_last_name="Smith")

    session.add(author)
    session.add(book)

    assert session.execute(
        select(Book, Author).where(
            col(Book.author_first_name) == Author.first_name,
            Book.author_last_name == Author.last_name,
        ),
    ).all() == [(book, author)]


def test_sa_kwargs(engine: Engine, session: Session) -> None:
    class Author(DBModel):
        first_name: str = mapped_column(
            sa_kwargs={"primary_key": True, "nullable": False},
        )
        last_name: str = mapped_column(sa_kwargs={"nullable": False})

    metadata.create_all(engine)

    author = Author(first_name="John", last_name=None)  # type: ignore
    session.add(author)
    with pytest.raises(IntegrityError):
        session.commit()


def test_invalid_model() -> None:
    with pytest.raises(
        RuntimeError, match=r"Unable to process type typing.Union\[str, datetime.date\]"
    ):

        @register
        class UnionType:
            name: Union[str, date]

    with pytest.raises(
        RuntimeError,
        match=r"Unable to process type typing.Union\[str, datetime.date, NoneType\]",
    ):

        @register
        class OptionalUnionType:
            name: Union[str, date, None]

    with pytest.raises(
        RuntimeError,
        match=r"Unable to map type typing.List",
    ):

        @register
        class ModelWithList:
            name: List


def test_overriden_transformer(session: Session, engine: Engine) -> None:
    class Author(DBModel):
        __transformer__ = pydantic.dataclasses.dataclass

        id: PrimaryKey[int]
        name: str
        age: Optional[int]

    assert hasattr(Author, "__pydantic_model__")
    with pytest.raises(pydantic.ValidationError):
        Author(id=1, name="Name", age="Invalid")  # type: ignore[arg-type]

    author = Author(id=1, name="Name", age=None)
    assert (
        json.dumps(
            author,
            default=pydantic.json.pydantic_encoder,
        )
        == '{"id": 1, "name": "Name", "age": null}'
    )

    metadata.create_all(engine)
    session.add(author)

    assert session.query(Author).all() == [author]


def test_inheritance(session: Session, engine: Engine) -> None:
    class Base(DBModel, abstract=True):
        id: PrimaryKey[int]
        name: str

    class Model1(Base):
        pass

    class Model2(Base):
        pass

    metadata.create_all(engine)
    assert len(metadata.tables) == 2

    session.add_all(
        [
            Model1(id=1, name="Hello"),
            Model2(id=1, name="Hello"),
            Model2(id=2, name="World"),
        ]
    )
    assert session.query(Model1).count() == 1
    assert session.query(Model2).count() == 2


def test_metadata() -> None:
    class Base(DBModel, abstract=True):
        id: PrimaryKey[int]
        name: str

    class Model1(Base, metadata=metadata):
        pass

    other_metadata = MetaData()

    class Model2(Base, metadata=other_metadata):
        pass

    assert len(metadata.tables) == 1
    assert len(other_metadata.tables) == 1
