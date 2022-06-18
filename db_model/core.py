from dataclasses import Field, dataclass, field, fields
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Iterable, Type, TypeVar

from sqlalchemy import Column, MetaData, Table
from sqlalchemy.orm import registry as Registry
from typing_extensions import Annotated, dataclass_transform

from db_model.field import Mapped as _Mapped
from db_model.field import mapped_column
from db_model.types_ import get_column

_T = TypeVar("_T")


if TYPE_CHECKING:
    Mapped = _Mapped
else:
    Mapped = Annotated[_T, "Mapped"]


_metadata = MetaData()
_default_registry = Registry()


def get_metadata() -> MetaData:
    return _metadata


def get_registry() -> Registry:
    return _default_registry


def get_columns(cls: type) -> Iterable[Column]:
    properties = getattr(cls, "__mapper_args__", {}).get("properties", {})
    fields_ = filter(lambda field: field.name not in properties, fields(cls))
    yield from map(get_column, fields_)


@dataclass_transform(
    field_descriptors=(field, Field, mapped_column),
    kw_only_default=True,
)
def register(
    cls: Type[_T],
    metadata: MetaData = _metadata,
    registry: Registry = _default_registry,
    abstract: bool = False,
) -> Type[_T]:
    transformer = getattr(cls, "__transformer__", dataclass)
    cls = transformer(cls)

    if not abstract:
        table_name = getattr(cls, "__tablename__", cls.__name__.lower())
        table_args = getattr(cls, "__table_args__", {})
        mapper_args = getattr(cls, "__mapper_args__", {})
        columns = get_columns(cls)

        registry.map_imperatively(
            cls,
            Table(
                table_name,
                metadata,
                *columns,
                *table_args,
            ),
            **mapper_args,
        )
    return cls


@dataclass_transform(
    field_descriptors=(field, Field, mapped_column),
    kw_only_default=True,
)
class DBModel:
    if TYPE_CHECKING:
        __table__: ClassVar[Table]
        __table_args__: ClassVar[tuple]
        __transformer__: ClassVar[Callable[[Type], Type]]
        __mapper_args__: ClassVar[Dict[str, Any]]

    def __init_subclass__(
        cls,
        *,
        metadata: MetaData = _metadata,
        registry: Registry = _default_registry,
        abstract: bool = False,
    ) -> None:
        register(
            cls,
            metadata=metadata,
            registry=registry,
            abstract=abstract,
        )
