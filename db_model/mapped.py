import typing
from dataclasses import MISSING, Field, dataclass, field, fields
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Literal,
    Mapping,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    overload,
)

from sqlalchemy import Column, Table, over
from sqlalchemy.orm import registry
from sqlalchemy.sql.elements import ColumnClause
from typing_extensions import Annotated

from db_model.types_ import get_type

_T = TypeVar("_T")


class Mapped(Generic[_T]):
    """Returns type for class attribute and actual value for instance."""

    if TYPE_CHECKING:

        @typing.overload
        def __get__(self, instance: Literal[None], owner: Any) -> ColumnClause[_T]:
            ...

        @typing.overload
        def __get__(self, instance: object, owner: Any) -> _T:
            ...

        def __get__(self, instance: object, owner: Any) -> Union[type[_T], _T]:
            ...

        def __set__(self, instance: Any, value: _T) -> None:
            ...

        def __delete__(self, instance: Any):
            ...


@overload
def mapped_column(
    *,
    default: _T,
    init: bool = ...,
    repr: bool = ...,
    hash: Optional[bool] = ...,
    compare: bool = ...,
    metadata: Optional[Mapping[str, Any]] = ...,
) -> Mapped[_T]:
    ...


@overload
def mapped_column(
    *,
    default_factory: Callable[[], _T],
    init: bool = ...,
    repr: bool = ...,
    hash: Optional[bool] = ...,
    compare: bool = ...,
    metadata: Optional[Mapping[str, Any]] = ...,
) -> Mapped[_T]:
    ...


@overload
def mapped_column(
    *,
    init: bool = ...,
    repr: bool = ...,
    hash: Optional[bool] = ...,
    compare: bool = ...,
    metadata: Optional[Mapping[str, Any]] = ...,
) -> Mapped[_T]:
    ...


def mapped_column(
    *,
    default=MISSING,
    default_factory=MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
) -> Mapped[_T]:
    return Field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
    )
