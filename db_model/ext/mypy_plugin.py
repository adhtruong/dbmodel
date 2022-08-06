from typing import Callable, Optional

from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins import dataclasses


class DBModelPlugin(Plugin):
    """Type checker plugin that is enabled by default."""

    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in {"db_model.core.register"}:
            return dataclasses.dataclass_class_maker_callback  # type: ignore[return-value]

        return None

    def get_base_class_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in {"db_model.core.DBModel"}:
            return dataclasses.dataclass_class_maker_callback  # type: ignore[return-value]

        return None


def plugin(_: str) -> type[Plugin]:
    return DBModelPlugin
