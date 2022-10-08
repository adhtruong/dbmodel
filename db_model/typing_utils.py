import sys
from typing import Any, Callable, Optional, Tuple, Type, Union, get_args, get_origin

from typing_extensions import Annotated, ParamSpec

if sys.version_info < (3, 10):

    def is_union(type_: Optional[Type[Any]]) -> bool:
        return type_ is Union

else:

    import types

    def is_union(tp: Optional[Type[Any]]) -> bool:
        return tp is Union or tp is types.UnionType  # noqa: E721


def get_sub_types(type_: Type) -> Tuple[Tuple[Type, ...], Tuple[Any, ...]]:
    origin = get_origin(type_)
    if origin is Annotated:
        args = get_args(type_)
        sub_types, _ = get_sub_types(args[0])
        return sub_types, args[1:]
    elif is_union(origin):
        return get_args(type_), ()
    else:
        return (type_,), ()


P = ParamSpec("P")


def copy_t(_: Callable[P, Any]) -> Callable[[Callable[..., Any]], Callable[P, Any]]:
    return lambda f: f
