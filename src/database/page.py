from __future__ import annotations

# ruff: noqa: D100, D101, D105
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Sequence

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page[T]:
    items: Sequence[T]
    total: int
    page: int
    size: int
    has_next: bool = field(init=False)
    has_previous: bool = field(init=False)
    total_pages: int = field(init=False)

    def __post_init__(self) -> None:
        total_pages = (self.total + self.size - 1) // self.size if self.size > 0 else 0
        object.__setattr__(self, "total_pages", total_pages)
        object.__setattr__(self, "has_next", self.page + 1 < total_pages)
        object.__setattr__(self, "has_previous", self.page > 0)
