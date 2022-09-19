from dataclasses import field
from typing import Any, ClassVar, List, Optional
from uuid import UUID, uuid4

from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship as sa_relationship

from db_model import DBModel, PrimaryKey
from db_model.core import _metadata as metadata
from db_model.field import mapped_column
from db_model.orm import Session
from db_model.relationship import relationship


def test_relationship_via_properties(session: Session, engine: Engine) -> None:
    class Author(DBModel):
        id: PrimaryKey[int]
        name: str
        age: Optional[int]

        books: List["Book"] = field(default_factory=list)

        __mapper_args__: ClassVar[dict[str, Any]] = {
            "properties": {
                "books": sa_relationship("Book", uselist=True),
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


def test_relationship(session: Session, engine: Engine) -> None:
    class Author(DBModel):
        id: PrimaryKey[UUID] = field(init=False, default_factory=uuid4)
        name: str
        age: int

        books: list["Book"] = relationship(
            "Book", back_populates="author", uselist=True
        )

    class Book(DBModel):
        id: PrimaryKey[int]
        name: str
        author_id: Optional[UUID] = mapped_column(default=None, foreign_key=Author.id)
        author: Author = relationship(Author, back_populates="books")

    metadata.create_all(engine)

    author = Author(name="My Author", age=20)
    book = Book(id=1, name="My Book", author=author)

    session.add_all((author, book))
    session.commit()
    session.refresh(author)
    assert author.books == [book]
