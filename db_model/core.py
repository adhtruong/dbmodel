from dataclasses import Field, dataclass, field, fields
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Iterable, TypeVar, Union

from sqlalchemy import Column, Table
from sqlalchemy.orm import registry
from typing_extensions import Annotated

from db_model.field import Mapped as _Mapped
from db_model.field import mapped_column
from db_model.types_ import get_column

_T = TypeVar("_T")


if TYPE_CHECKING:
    Mapped = _Mapped
else:
    Mapped = Annotated[_T, "Mapped"]


PrimaryKey = Annotated[_T, "PrimaryKey"]

mapper_registry = registry()


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


def get_columns(cls) -> Iterable[Column]:
    yield from map(get_column, fields(cls))


@__dataclass_transform__(
    field_descriptors=(field, Field, mapped_column),
    kw_only_default=True,
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
            *table_args,
        ),
    )
    return cls


@__dataclass_transform__(
    field_descriptors=(field, Field, mapped_column),
    kw_only_default=True,
)
class DBModel:
    if TYPE_CHECKING:
        __table__: ClassVar[Table]
        __table_args__: ClassVar[tuple]

    def __init_subclass__(cls) -> None:
        register(cls)
