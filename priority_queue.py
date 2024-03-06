from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar


T = TypeVar("T")


@dataclass(frozen=True, order=True, slots=True)
class Element:
    value: T = field(compare=False)
    key: int
