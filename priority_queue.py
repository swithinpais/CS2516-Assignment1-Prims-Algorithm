from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T")


@dataclass(order=True, slots=True)
class Element:
    key: int
    value: T = field(compare=False)
    index: int = field(compare=False)


class APQ(ABC):
    def __init__(self) -> None:
        self._queue: list[Element] = []

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(self._queue)})"

    def length(self) -> int:
        """Returns the length of the queue.

        Returns:
            int: The length of the queue.
        """
        return len(self._queue)

    def get_key(self, element: Element) -> int:
        return element.key

    @abstractmethod
    def min(self) -> T:
        """Returns the highest priority item.

        Returns:
            T: The item with the highest priority.
        """

    @abstractmethod
    def add(self, key: int, value: T) -> Element:
        """Adds an item to the queue.

        Args:
            key (int): The priority of the item. Smaller numbers are higher priority.
            value (T): The value of the item to be added.
        """

    @abstractmethod
    def remove_min(self) -> T:
        """Returns and removes the item with highest priority.

        Returns:
            T: The item with highest priority.
        """

    @abstractmethod
    def update_key(self, element: Element, key: int) -> None:
        """Update the element's priority.

        Args:
            element (Element): The element to be updated.
            key (int): The new priority of the element.
        """

    @abstractmethod
    def remove(self, element: Element) -> tuple[int, T]:
        """Remove the element

        Args:
            element (Element): The element to be removed.

        Returns:
            tuple[int, T]: A (key, value) pair of the element's key and value.
        """


class HeapAPQ(APQ):
    def _bubble_down(self, i: int) -> None:
        n = self.length() - 1
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            if l > n:
                break
            if r > n:
                if self._queue[i] < self._queue[r]:
                    break
                self._queue[i], self._queue[r] = self._queue[r], self._queue[i]
                self._queue[i].index, self._queue[r].index = i, r
                i = r
            elif self._queue[l] < self._queue[r]:
                if self._queue[i] < self._queue[l]:
                    break
                else:
                    self._queue[i], self._queue[l] = self._queue[l], self._queue[i]
                self._queue[i].index, self._queue[r].index = i, l
            elif self._queue[i] < self._queue[r]:
                break
            else:
                self._queue[i], self._queue[r] = self._queue[r], self._queue[i]
                self._queue[i].index, self._queue[r].index = i, r

    def _bubble_up(self, i: int) -> None:
        while (self._queue[(i - 1) // 2] > self._queue[i]):
            self._queue[i], self._queue[(i - 1) // 2] = \
                self._queue[(i - 1) // 2], self._queue[i]
            self._queue[i].index = i
            self._queue[(i - 1) // 2] = (i - 1) // 2
            i = (i - 1) // 2

    def min(self) -> T:
        return self._queue[0].value

    def add(self, key: int, value: T) -> Element:
        e = Element(key, value)
        self._queue.append(e)

        self._bubble_up(self.length() - 1)

        return e

    def remove_min(self) -> T:
        n = self.length() - 1
        self._queue[0], self._queue[n] = self._queue[n], self._queue[0]

        e = self._queue.pop(self.length() - 1)

        self._bubble_down(0)

        return e.value

    def update_key(self, element: Element, key: int) -> None:
        old_key = element.key
        element.key = key
        if old_key > key:
            self._bubble_up(element.index)
        else:
            self._bubble_down(element.index)

    def remove(self, element: Element) -> tuple[int, T]:
        n = self.length() - 1
        self._queue[element.index], self._queue[n] = self._queue[n], self._queue[element.index]

        self._bubble_down(element.index)
        self._bubble_up(element.index)

        return element.key, element.value


class UnsortedListAPQ(APQ):
    def add(self, key: int, value: T) -> Element:
        e = Element(key, value, self.length())
        self._queue.append(e)
        return e

    def min(self) -> T:
        e = self._queue[0]
        for v in self._queue:
            if v < e:
                e = v
        return e

    def remove_min(self) -> T:
        e = self._queue[0]
        for v in self._queue:
            if v < e:
                e = v
        self._swap_with_end(e)
        t = self._queue.pop()
        return t.value

    def update_key(self, element: Element, key: int) -> None:
        element.key = key

    def remove(self, element: Element) -> tuple[int, T]:
        self._swap_with_end(element)
        self._queue.pop()

    # TODO Rename this here and in `remove_min` and `remove`
    def _swap_with_end(self, element: Element):
        n = self.length() - 1
        self._queue[element.index], self._queue[n] = self._queue[n], self._queue[element.index]
        self._queue[element.index].index = element.index
