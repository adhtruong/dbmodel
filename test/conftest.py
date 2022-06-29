from typing import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from db_model import get_metadata, get_registry
from db_model.orm import Session

metadata = get_metadata()


@pytest.fixture(name="engine")
def fixture_engine() -> Engine:
    return create_engine("sqlite:///:memory:", future=True)


@pytest.fixture(name="session")
def fixture_session(engine: Engine) -> Iterator[Session]:
    registry = get_registry()
    registry.dispose()
    metadata.clear()

    connection = engine.connect()
    with Session(bind=connection) as session:
        yield session

    registry.dispose()
    metadata.clear()
