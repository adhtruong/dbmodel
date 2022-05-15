from db_model import DBModel, PrimaryKey, register


class MyModel(DBModel):
    id: PrimaryKey[int]
    name: str


@register
class OtherModel:
    id: PrimaryKey[int]
    name: str


MyModel(id=1, name="hello")
