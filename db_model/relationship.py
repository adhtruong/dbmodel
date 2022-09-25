from dataclasses import MISSING, Field
from typing import Any, Dict, TypeVar

from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm import relationship as _relationship

from db_model.dataclass_utils import KW_ONLY
from db_model.typing_utils import copy_t

T = TypeVar("T")


class RelationshipInfo(Field[T]):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        field_kwargs: Dict[str, Any] = dict(
            default=None,
            default_factory=MISSING,
            init=True,
            repr=False,
            hash=False,
            compare=False,
            metadata=None,
            **KW_ONLY,
        )
        if kwargs.get("uselist", False):
            field_kwargs.update(
                default=MISSING,
                default_factory=list,
            )

        super().__init__(**field_kwargs)  # type: ignore
        self.args = args
        self.kwargs = kwargs

    def __getrelationship__(self) -> RelationshipProperty:
        return _relationship(*self.args, **self.kwargs)


@copy_t(_relationship)
def relationship(*args, **kwargs) -> Any:
    return RelationshipInfo(*args, **kwargs)
