import json
from dataclasses import field
from datetime import date
from typing import Any, ClassVar, Iterator, List, Optional, Union
from uuid import UUID, uuid4

import pydantic
import pytest
from sqlalchemy import ForeignKeyConstraint, MetaData, Table, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, relationship

from db_model import Mapped, PrimaryKey, register
from db_model.core import DBModel, _default_registry, get_metadata
from db_model.field import col, mapped_column

metadata = get_metadata()


@pytest.fixture(name="engine")
def fixture_engine() -> Engine:
    return create_engine("sqlite:///:memory:", future=True)


@pytest.fixture(name="session")
def fixture_session(engine: Engine) -> Iterator[Session]:
    _default_registry.dispose()
    metadata.clear()

    connection = engine.connect()
    with Session(bind=connection) as session:
        yield session

    _default_registry.dispose()
    metadata.clear()


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

    assert session.execute(select(Model)).scalars().all() == models
    assert session.execute(select(Model).where(Model.age == None)).scalars().all() == models[:1]  # noqa: E711
    assert session.execute(select(Model).where(Model.age == 20)).scalars().all() == models[1:]

    updated_model: Model = session.execute(select(Model).filter(Model.age == 20)).scalar_one()
    updated_model.age = 25
    session.add(updated_model)

    assert session.get(Model, updated_model.id) == updated_model
    assert session.execute(select(Model).where(Model.age == 20)).all() == []
    assert set(session.execute(select(col(Model.id))).all()) == {(model.id,) for model in models}


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


def test_relationship(session: Session, engine: Engine) -> None:
    class Author(DBModel):
        id: PrimaryKey[int]
        name: str
        age: Optional[int]

        books: List["Book"] = field(default_factory=list)  # noqa: F821

        __mapper_args__: ClassVar[dict[str, Any]] = {
            "properties": {
                "books": relationship("Book"),
            }
        }

    class Book(DBModel):
        id: PrimaryKey[int]
        name: str
        author_id: int = mapped_column(foreign_key=Author.id)

    metadata.create_all(engine)

    author = Author(id=1, name="My Author", age=20)
    book = Book(id=1, name="My Book", author_id=author.id)

    session.add_all((author, book))
    session.commit()
    session.refresh(author)
    assert author.books == [book]
