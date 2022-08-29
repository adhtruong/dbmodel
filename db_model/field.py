from dataclasses import MISSING
from dataclasses import Field as _Field
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    Generic,
    Literal,
    Mapping,
    Optional,
    Tuple,
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

        @overload
        def __get__(
            self, instance: Literal[None], owner: Any
        ) -> ColumnClause[TypeEngine[_T]]:
            ...

        @overload
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


class Field(_Field, Generic[_T]):
    def __init__(
        self,
        default,
        default_factory,
        init,
        repr,
        hash,
        compare,
        metadata,
        primary_key: bool,
        foreign_key: Optional[Union[str, ForeignKey, PrimaryKey[_T]]],
        sa_args: Optional[Tuple[Any, ...]],
        sa_kwargs: Optional[Mapping[str, Any]],
    ) -> None:
        super().__init__(
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
        )
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.sa_args = sa_args
        self.sa_kwargs = sa_kwargs


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
    sa_args: Optional[Tuple[Any, ...]] = ...,
    sa_kwargs: Optional[Mapping[str, Any]] = ...,
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
    sa_args: Optional[Tuple[Any, ...]] = ...,
    sa_kwargs: Optional[Mapping[str, Any]] = ...,
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
    sa_args: Optional[Tuple[Any, ...]] = ...,
    sa_kwargs: Optional[Mapping[str, Any]] = ...,
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
    sa_args: Optional[Tuple[Any, ...]] = None,
    sa_kwargs: Optional[Mapping[str, Any]] = None,
) -> _T:
    return Field(  # type: ignore[return-value]
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        primary_key=is_primary_key,
        foreign_key=foreign_key,
        sa_args=sa_args,
        sa_kwargs=sa_kwargs,
    )


def col(c: Union[PrimaryKey[_T], Mapped[_T], _T], /) -> ColumnClause[TypeEngine[_T]]:
    return c  # type: ignore[return-value]
