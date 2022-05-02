"""Utils and wrappers for SQLAlchemy."""

__version__ = "0.0.0"

__all__ = (
    "register",
    "Mapped",
    "PrimaryKey",
    "mapped_column",
)

from .core import Mapped, register
from .field import PrimaryKey, mapped_column
