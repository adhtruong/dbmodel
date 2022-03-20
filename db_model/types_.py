import uuid
from datetime import date, datetime
from typing import Any, Dict, Type, Union, get_args, get_origin

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.types import TypeDecorator, TypeEngine
from sqlalchemy_utils.types.json import JSONType  # type: ignore
from sqlalchemy_utils.types.uuid import UUIDType  # type: ignore

_COLUMN_TYPE_MAPPING: Dict[Type[Any], Type[TypeEngine]] = {
    int: Integer,
    str: String,
    date: Date,
    datetime: DateTime,
    dict: JSONType,
    uuid.UUID: UUIDType,
}


def register_type(type_: Type, db_type: type[TypeDecorator]) -> None:
    _COLUMN_TYPE_MAPPING[type_] = db_type


def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


def get_type(type_: type) -> TypeEngine:
    if not is_optional(type_):
        return _COLUMN_TYPE_MAPPING[type_]()

    inner_types = {inner_type for inner_type in get_args(type_) if type_ != type(None)}  # noqa: E721
    if len(inner_types) != 1:
        raise RuntimeError(f"Unable to process {type_}")
    actual_type = tuple(inner_types)[0]
    return _COLUMN_TYPE_MAPPING[actual_type]().evaluates_none()
