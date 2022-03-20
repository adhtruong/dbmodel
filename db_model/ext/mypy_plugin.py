from typing import Callable, Optional

from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins import dataclasses


class DBModelPlugin(Plugin):
    """Type checker plugin that is enabled by default."""

    def get_class_decorator_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:

        if fullname in {"db_model.core.register"}:
            return dataclasses.dataclass_class_maker_callback

        return None


def plugin(_: str) -> type[Plugin]:
    return DBModelPlugin
