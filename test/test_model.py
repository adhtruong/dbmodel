from dataclasses import field
from typing import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from db_model import register
from db_model.core import mapper_registry


@pytest.fixture(name="engine")
def fixture_engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture(name="session")
def fixture_session(engine: Engine) -> Iterator[Session]:
    connection = engine.connect()
    with Session(bind=connection) as session:
        yield session


def test_simple_model(engine: Engine, session: Session) -> None:
    @register
    class Model:
        id: int = field(metadata={"primary_key": True})

    mapper_registry.metadata.create_all(engine)

    model = Model(id=1)
    session.add(model)

    assert session.query(Model).all() == [Model(id=1)]
