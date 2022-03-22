import uuid
from dataclasses import Field, dataclass
from datetime import date, datetime
from typing import Any, Dict, Type, Union, get_args, get_origin

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.types import TypeDecorator, TypeEngine
from sqlalchemy_utils.types.json import JSONType  # type: ignore
from sqlalchemy_utils.types.uuid import UUIDType  # type: ignore
from typing_extensions import Annotated

_COLUMN_TYPE_MAPPING: Dict[Type[Any], Type[TypeEngine]] = {
    int: Integer,
    str: String,
    date: Date,
    datetime: DateTime,
    dict: JSONType,
    uuid.UUID: UUIDType,
}


@dataclass(frozen=True)
class ColumnInfo:
    type_: TypeEngine
    is_optional: bool
    is_primary_key: bool


def register_type(type_: Type, db_type: type[TypeDecorator]) -> None:
    _COLUMN_TYPE_MAPPING[type_] = db_type


def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


def get_type(field: Field) -> ColumnInfo:
    is_annotated = get_origin(field.type) is not Annotated
    type_ = field.type if is_annotated else get_args(field.type)[0]
    is_primary_key = field.metadata.get("primary_key", False) or "PrimaryKey" in get_args(field.type)[1:]

    if not is_optional(type_):
        try:
            return ColumnInfo(
                _COLUMN_TYPE_MAPPING[type_](),
                is_optional=False,
                is_primary_key=is_primary_key,
            )
        except KeyError:
            raise RuntimeError(f"Unable to map type {type_}")

    inner_types = {inner_type for inner_type in get_args(type_) if inner_type != type(None)}  # noqa: E721
    if len(inner_types) != 1:
        raise RuntimeError(f"Unable to process {type_}: {inner_types}")
    actual_type = tuple(inner_types)[0]
    return ColumnInfo(
        _COLUMN_TYPE_MAPPING[actual_type]().evaluates_none(),
        is_optional=True,
        is_primary_key=is_primary_key,
    )
