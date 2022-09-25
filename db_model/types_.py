import uuid
from dataclasses import Field
from datetime import date, datetime
from typing import Any, Dict, Tuple, Type, TypeVar, Union

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.types import TypeDecorator, TypeEngine

from db_model.sa_types import GUID
from db_model.typing_utils import get_sub_types

_T = TypeVar("_T")

_COLUMN_TYPE_MAPPING: Dict[Type, Type[Union[TypeDecorator, TypeEngine]]] = {
    int: Integer,
    str: String,
    date: Date,
    datetime: DateTime,
    uuid.UUID: GUID,
}


def register_type(
    type_: Type[_T], db_type: Type[TypeDecorator[_T]]
) -> None:  # pragma: no cover
    _COLUMN_TYPE_MAPPING[type_] = db_type


def get_column_type(field: Field[_T]) -> TypeEngine[_T]:
    sub_types, _ = get_sub_types(field.type)
    inner_types = {
        inner_type for inner_type in sub_types if not isinstance(None, inner_type)
    }
    if len(inner_types) != 1:
        raise RuntimeError(f"Unable to process type {field.type}: {inner_types}")
    actual_type = tuple(inner_types)[0]
    try:
        column_type = _COLUMN_TYPE_MAPPING[actual_type]()
    except KeyError:
        raise RuntimeError(f"Unable to map type {field.type}: {inner_types}")

    return column_type


def get_column(field: Field[_T]) -> Column[TypeEngine[_T]]:
    args: Tuple[Any, ...] = getattr(field, "sa_args", None) or ()
    foreign_key = getattr(field, "foreign_key", None)
    if foreign_key is not None:
        foreign_key = (
            ForeignKey(foreign_key)
            if not isinstance(foreign_key, ForeignKey)
            else foreign_key
        )
        args += (foreign_key,)

    column_type = get_column_type(field)

    sub_types, annotations = get_sub_types(field.type)
    is_primary_key = getattr(field, "primary_key", False) or "PrimaryKey" in annotations
    kwargs: Dict[str, Union[str, Any]] = {
        "nullable": type(None) in sub_types,
        "primary_key": is_primary_key,
    }
    kwargs.update(getattr(field, "sa_kwargs", None) or {})

    return Column(
        field.name,
        column_type,
        *args,
        **kwargs,  # type: ignore
    )
