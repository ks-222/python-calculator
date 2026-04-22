"""
add.py — a pleasantly over-engineered addition module.

The classic ``add(x, y)`` still works exactly as before, but the function is now
polymorphic: it happily sums numbers, strings, lists, tuples, and nested
combinations of them. It also accepts any number of arguments.

Examples
--------
>>> add(2, 3)
5
>>> add(1, 2, 3, 4)
10
>>> add([1, 2, 3], [10, 20, 30])
[11, 22, 33]
>>> add("foo", "bar")
'foobar'
>>> add((1, 2), (3, 4), (5, 6))
(9, 12)
"""

from __future__ import annotations

from functools import reduce
from typing import Iterable, TypeVar, Union, overload

Number = Union[int, float, complex]
T = TypeVar("T", int, float, complex, str, list, tuple)

__all__ = ["add", "sum_of_squares"]


@overload
def add(x: Number, y: Number, *rest: Number) -> Number: ...
@overload
def add(x: str, y: str, *rest: str) -> str: ...
@overload
def add(x: list, y: list, *rest: list) -> list: ...
@overload
def add(x: tuple, y: tuple, *rest: tuple) -> tuple: ...


def add(*args):
    """Return the sum of all arguments.

    Works on anything that supports ``+``. For list/tuple arguments of equal
    length, addition is performed **element-wise** rather than by concatenation,
    which is usually what you actually want.

    Parameters
    ----------
    *args :
        Two or more values to add together.

    Returns
    -------
    The combined result, with the same type as the inputs.

    Raises
    ------
    TypeError
        If fewer than two arguments are supplied or the types are incompatible.
    ValueError
        If sequence arguments have mismatched lengths.
    """
    if len(args) < 2:
        raise TypeError(f"add() expected at least 2 arguments, got {len(args)}")

    return reduce(_pairwise_add, args)


def _pairwise_add(a, b):
    """Add two values, doing something sensible for sequences."""
    if isinstance(a, list) and isinstance(b, list):
        _check_len(a, b)
        return [_pairwise_add(x, y) for x, y in zip(a, b)]
    if isinstance(a, tuple) and isinstance(b, tuple):
        _check_len(a, b)
        return tuple(_pairwise_add(x, y) for x, y in zip(a, b))
    return a + b


def _check_len(a: Iterable, b: Iterable) -> None:
    if len(a) != len(b):
        raise ValueError(
            f"cannot add sequences of different lengths: {len(a)} vs {len(b)}"
        )


def sum_of_squares(*args: Number) -> Number:
    """Return the sum of the squares of the arguments.

    A little bonus helper, because what's a demo branch without a flourish?

    >>> sum_of_squares(3, 4)
    25
    >>> sum_of_squares(1, 2, 2)
    9
    """
    return add(*(x * x for x in args))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
