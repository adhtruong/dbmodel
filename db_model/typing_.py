import sys
from typing import Any, Optional, Type, Union, get_args, get_origin

from typing_extensions import Annotated

if sys.version_info < (3, 10):  # pragma: no cover

    def is_union(type_: Optional[Type[Any]]) -> bool:
        return type_ is Union

else:  # pragma: no cover

    import types

    def is_union(tp: Optional[Type[Any]]) -> bool:
        return tp is Union or tp is types.UnionType  # noqa: E721


def get_sub_types(type_: type) -> tuple[tuple[type, ...], tuple[Any, ...]]:
    origin = get_origin(type_)
    if origin is Annotated:
        args = get_args(type_)
        sub_types, _ = get_sub_types(args[0])
        return sub_types, args[1:]
    elif is_union(origin):
        return get_args(type_), ()
    else:
        return (type_,), ()
