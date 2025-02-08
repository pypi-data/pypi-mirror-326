from .model import BaseModel
from _typeshed import Incomplete
from typing import Generic, TypeVar

T = TypeVar('T')

class GenericStateErrorStatus(BaseModel, Generic[T]):
    model_config: Incomplete
    state: T | None
