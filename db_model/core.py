from dataclasses import Field, dataclass
from dataclasses import field as _field
from dataclasses import fields
from typing import Any, Callable, Iterable, TypeVar, Union

from sqlalchemy import Column, Table
from sqlalchemy.orm import registry

from db_model.types_ import get_type

mapper_registry = registry()


_T = TypeVar("_T")


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    # If used within a stub file, the following implementation can be
    # replaced with "...".
    return lambda a: a


@__dataclass_transform__(
    kw_only_default=False,
    field_descriptors=(_field, Field),
)
def register(cls: type[_T]) -> type[_T]:
    cls = dataclass(cls)
    table_name = getattr(cls, "__tablename__", cls.__name__.lower())
    table_args = getattr(cls, "__table_args__", {})
    columns = get_columns(cls)

    mapper_registry.map_imperatively(
        cls,
        Table(
            table_name,
            mapper_registry.metadata,
            *columns,
            **table_args,
        ),
    )
    return cls


def get_columns(cls) -> Iterable[Column]:
    for field in fields(cls):
        yield Column(
            field.name,
            get_type(field.type),
            primary_key=field.metadata.get("primary_key", False),
        )
