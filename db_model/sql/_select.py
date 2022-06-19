from typing import Any, Generic, TypeVar, overload

from sqlalchemy.sql import Select as _Select
from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.types import TypeEngine

Ts = TypeVar("Ts", bound=tuple)


class Select(_Select, Generic[Ts]):
    inherit_cache = True


_TVal_0 = TypeVar("_TVal_0")
_TVal_1 = TypeVar("_TVal_1")
_TVal_2 = TypeVar("_TVal_2")


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    entity_1: type[_TVal_1],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    value_1: _TVal_1,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    entity_1: type[_TVal_1],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    value_1: _TVal_1,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    entity_1: type[_TVal_1],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    value_1: _TVal_1,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    entity_1: type[_TVal_1],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    entity_1: type[_TVal_1],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    entity_1: type[_TVal_1],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    value_1: _TVal_1,
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    value_1: _TVal_1,
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    column_0: ColumnClause[TypeEngine[_TVal_0]],
    value_1: _TVal_1,
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    entity_1: type[_TVal_1],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    entity_1: type[_TVal_1],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    entity_1: type[_TVal_1],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    value_1: _TVal_1,
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    value_1: _TVal_1,
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    entity_0: type[_TVal_0],
    value_1: _TVal_1,
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    column_1: ColumnClause[TypeEngine[_TVal_1]],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    entity_1: type[_TVal_1],
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    entity_1: type[_TVal_1],
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    entity_1: type[_TVal_1],
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    value_1: _TVal_1,
    column_2: ColumnClause[TypeEngine[_TVal_2]],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    value_1: _TVal_1,
    entity_2: type[_TVal_2],
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


@overload
def select(
    value_0: _TVal_0,
    value_1: _TVal_1,
    value_2: _TVal_2,
    /,
    **kw: Any,
) -> Select[tuple[_TVal_0, _TVal_1, _TVal_2]]:
    ...


def select(*entities: Any, **kw: Any) -> Select:  # type: ignore
    return Select._create(*entities, **kw)  # type: ignore[return-value]
