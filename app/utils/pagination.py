from typing import List, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
