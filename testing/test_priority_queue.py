import sys

from src.priority_queue import HeapAPQ, UnsortedListAPQ, APQ, Element

import pytest

py310 = sys.version_info.minor >= 10 or sys.version_info.major > 3


@pytest.mark.parametrize("apq_class", [HeapAPQ, UnsortedListAPQ])
def test_apq(apq_class: APQ):
    apq: APQ = apq_class()

    items = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    for item in items:
        e = apq.add(item, item)

    assert apq.length() == 10

    assert apq.min() == 0

    assert apq.remove_min() == 0

    apq.remove_min()
    apq.remove_min()

    assert apq.min() == 3

    e2 = apq.add(1, 1)

    assert apq.min() == 1

    assert apq.get_key(e) == 9

    assert apq.remove(e) == (9, 9)

    apq.update_key(e2, 10)

    assert apq.min() == 3

    apq.update_key(e2, 0)

    assert apq.min() == 1

    apq = apq_class()

    with pytest.raises(IndexError):
        apq.remove_min()

    with pytest.raises(IndexError):
        apq.remove(e)


def test_apq_abc():
    with pytest.raises(TypeError):
        apq = APQ()


def test_element():
    e1 = Element(1, 1, 1)

    e2 = Element(1, 2, 2)

    assert e1 == e2

    e3 = Element(2, 3, 3)

    assert e2 < e3

    if py310:
        with pytest.raises(AttributeError):
            e3.new_attr = 5
