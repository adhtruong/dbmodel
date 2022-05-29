import sys
from typing import Any, Optional, Tuple, Type, Union, cast, get_args
from typing import get_origin as _typing_get_origin

from typing_extensions import Annotated

if sys.version_info < (3, 10):  # pragma: no cover

    def is_union(type_: Optional[Type[Any]]) -> bool:
        return type_ is Union

else:  # pragma: no cover

    import types

    def is_union(tp: Optional[Type[Any]]) -> bool:
        return tp is Union or tp is types.UnionType  # noqa: E721


AnnotatedTypeNames = {"AnnotatedMeta", "_AnnotatedAlias"}


def get_origin(tp: Type[Any]) -> Optional[Type[Any]]:
    """
    We can't directly use `typing.get_origin` since we need a fallback to support
    custom generic classes like `ConstrainedList`
    It should be useless once https://github.com/cython/cython/issues/3537 is
    solved and https://github.com/samuelcolvin/pydantic/pull/1753 is merged.
    """
    if type(tp).__name__ in AnnotatedTypeNames:
        return cast(Type[Any], Annotated)  # mypy complains about _SpecialForm
    return _typing_get_origin(tp) or getattr(tp, "__origin__", None)


def get_sub_types(type_: type) -> Tuple[Tuple[type, ...], Tuple[Any, ...]]:
    origin = get_origin(type_)
    if origin is Annotated:
        args = get_args(type_)
        sub_types, _ = get_sub_types(args[0])
        return sub_types, args[1:]
    elif is_union(origin):
        return get_args(type_), ()
    else:
        return (type_,), ()
