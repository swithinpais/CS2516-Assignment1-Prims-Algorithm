from __future__ import annotations

"""
Provided by MCoding. https://www.youtube.com/@mCoding
Source Code: https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/101_zip_dict/zip_dict.py

MIT License

Copyright (c) 2022 MCODING, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from collections.abc import Iterator, Mapping
from typing import TypeVar, overload

_K = TypeVar('_K')

_V1 = TypeVar('_V1')
_V2 = TypeVar('_V2')
_V3 = TypeVar('_V3')


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
) -> Iterator[tuple[_K, _V1]]:
    ...


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
        m2: Mapping[_K, _V2],
) -> Iterator[tuple[_K, _V1, _V2]]:
    ...


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
        m2: Mapping[_K, _V2],
        m3: Mapping[_K, _V3],
) -> Iterator[tuple[_K, _V1, _V2, _V3]]:
    ...


def dict_zip(*dicts):
    if not dicts:
        return

    n = len(dicts[0])
    if any(len(d) != n for d in dicts):
        raise ValueError('arguments must have the same length')

    for key, first_val in dicts[0].items():
        yield key, first_val, *(other[key] for other in dicts[1:])


def dict_zip_intersection(*dicts):
    if not dicts:
        return

    keys = set(dicts[0]).intersection(*dicts[1:])
    for key in keys:
        yield key, *(d[key] for d in dicts)


def dict_zip_union(*dicts, fillvalue=None):
    if not dicts:
        return

    keys = set(dicts[0]).union(*dicts[1:])
    for key in keys:
        yield key, *(d.get(key, fillvalue) for d in dicts)
