import typing
from dataclasses import MISSING, field
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    Generic,
    Literal,
    Mapping,
    Optional,
    TypeVar,
    Union,
    overload,
)

from sqlalchemy import ForeignKey
from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.types import TypeEngine

_T = TypeVar("_T")

PrimaryKey = Annotated[_T, "PrimaryKey"]


class Mapped(Generic[_T]):
    """Returns type for class attribute and actual value for instance."""

    if TYPE_CHECKING:

        @typing.overload
        def __get__(self, instance: Literal[None], owner: Any) -> ColumnClause[TypeEngine[_T]]:
            ...

        @typing.overload
        def __get__(self, instance: object, owner: Any) -> _T:
            ...

        def __get__(
            self,
            instance: object,
            owner: Any,
        ) -> Union[ColumnClause[TypeEngine[_T]], _T]:
            ...

        def __set__(self, instance: Any, value: _T) -> None:
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
    is_primary_key: bool = False,
    foreign_key: Optional[Union[str, ForeignKey, PrimaryKey[_T]]] = ...,
) -> _T:
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
    is_primary_key: bool = False,
    foreign_key: Optional[Union[str, ForeignKey, PrimaryKey[_T]]] = ...,
) -> _T:
    ...


@overload
def mapped_column(
    *,
    init: bool = ...,
    repr: bool = ...,
    hash: Optional[bool] = ...,
    compare: bool = ...,
    metadata: Optional[Mapping[str, Any]] = ...,
    is_primary_key: bool = False,
    foreign_key: Optional[Union[str, ForeignKey, PrimaryKey[_T]]] = ...,
) -> _T:
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
    is_primary_key: bool = False,
    foreign_key: Optional[Union[str, ForeignKey, PrimaryKey[_T]]] = None,
) -> _T:
    if metadata is None:
        metadata = {}
    return field(  # type: ignore[call-overload,return-value]
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata
        | {
            "is_primary_key": is_primary_key,
            "foreign_key": foreign_key,
        },
    )


def col(c: _T, /) -> ColumnClause[TypeEngine[_T]]:
    return c  # type: ignore[return-value]
