from typing import Any, Mapping, Optional, Sequence, TypeVar, Union, overload

from sqlalchemy import util
from sqlalchemy.orm import Session as _Session
from sqlalchemy.sql.base import Executable

from db_model.engine.result import Result, ScalarResult
from db_model.sql import Select

_TSelect = TypeVar("_TSelect")
_TSelect0 = TypeVar("_TSelect0")

_TSelectParam = TypeVar("_TSelectParam", bound=tuple)


class Session(_Session):
    @overload  # type: ignore[override]
    def scalars(
        self,
        statement: Select[tuple[_TSelect]],
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult[_TSelect]:
        ...

    @overload  # type: ignore[override]
    def scalars(
        self,
        statement: Select[tuple[_TSelect, _TSelect0]],
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult[_TSelect]:
        ...

    @overload
    def scalars(
        self,
        statement: Executable,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult:
        ...

    def scalars(
        self,
        statement: Union[Executable, Select[tuple]],
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult:
        return super().scalars(statement, params, execution_options, bind_arguments, **kw)  # type: ignore[return-value]

    @overload  # type: ignore[override]
    def execute(
        self,
        statement: Select[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Result[_TSelectParam]:
        ...

    @overload
    def execute(
        self,
        statement: Executable,
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Result[_TSelectParam]:
        ...

    def execute(
        self,
        statement: Union[Executable, Select[_TSelectParam]],
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Union[Result[_TSelectParam], ScalarResult[_TSelectParam]]:
        return super().execute(  # type: ignore[return-value]
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
            **kw,
        )
