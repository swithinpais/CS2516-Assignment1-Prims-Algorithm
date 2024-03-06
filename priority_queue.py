from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar


T = TypeVar("T")


@dataclass(frozen=True, order=True, slots=True)
class Element:
    key: int
    value: T = field(compare=False)


class APriorityQueue:
    def __init__(self) -> None:
        self._queue: list[Element] = []

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f""

    def min(self) -> T:
        return self._queue[0].value

    def length(self) -> int:
        return len(self._queue)

    def add(self, key: int, value: T) -> None:
        e = Element(key, value)
        self._queue.append(e)
        i = self.length() - 1
        while (self._queue[(i - 1) // 2] > e):
            self._queue[i], self._queue[(i - 1) // 2] = \
                self._queue[(i - 1) // 2], self._queue[i]
            i = (i - 1) // 2

    def remove_min(self) -> T:
        n = self.length() - 1
        self._queue[0], self._queue[n] = self._queue[n], self._queue[0]

        e = self.pop(self.length() - 1)

        i = 0
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            if l > n:
                break
            if r > n:
                if self._queue[i] < self._queue[r]:
                    break
                self._queue[i], self._queue[r] = self._queue[r], self._queue[i]
                i = r
            elif self._queue[l] < self._queue[r]:
                if self._queue[i] < self._queue[l]:
                    break
                else:
                    self._queue[i], self._queue[l] = self._queue[l], self._queue[i]
            elif self._queue[i] < self._queue[r]:
                break
            else:
                self._queue[i], self._queue[r] = self._queue[r], self._queue[i]
