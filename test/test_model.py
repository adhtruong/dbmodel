from dataclasses import field

from db_model import register


def test_simple_model() -> None:
    @register
    class Model:
        id: int = field(metadata={"primary_key": True})

    model = Model(id=1)
    assert model.id == 1
