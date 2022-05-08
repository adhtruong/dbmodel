import uuid
from dataclasses import Field
from datetime import date, datetime
from typing import Dict, Type, TypeVar, Union, get_args, get_origin

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.types import TypeDecorator, TypeEngine
from typing_extensions import Annotated

from db_model.sa_types import GUID

_T = TypeVar("_T")

_COLUMN_TYPE_MAPPING: Dict[Type, Type[Union[TypeDecorator, TypeEngine]]] = {
    int: Integer,
    str: String,
    date: Date,
    datetime: DateTime,
    uuid.UUID: GUID,
}


def register_type(type_: type[_T], db_type: type[TypeDecorator[_T]]) -> None:
    _COLUMN_TYPE_MAPPING[type_] = db_type


def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


def get_column(field: Field) -> Column[TypeEngine[_T]]:
    is_annotated = get_origin(field.type) is not Annotated
    type_ = field.type if is_annotated else get_args(field.type)[0]
    is_primary_key = field.metadata.get("is_primary_key", False) or "PrimaryKey" in get_args(field.type)[1:]

    args: tuple = ()
    foreign_key = field.metadata.get("foreign_key")
    if foreign_key is not None:
        if not isinstance(foreign_key, ForeignKey):
            foreign_key = ForeignKey(foreign_key)
        args += (foreign_key,)

    if not is_optional(type_):
        try:
            return Column(
                field.name,
                _COLUMN_TYPE_MAPPING[type_](),
                *args,
                nullable=False,
                primary_key=is_primary_key,
            )
        except KeyError:
            raise RuntimeError(f"Unable to map type {type_}")

    inner_types = {inner_type for inner_type in get_args(type_) if inner_type != type(None)}  # noqa: E721
    if len(inner_types) != 1:
        raise RuntimeError(f"Unable to process {type_}: {inner_types}")
    actual_type = tuple(inner_types)[0]
    return Column(
        field.name,
        _COLUMN_TYPE_MAPPING[actual_type]().evaluates_none(),
        *args,
        nullable=True,
        primary_key=is_primary_key,
    )
