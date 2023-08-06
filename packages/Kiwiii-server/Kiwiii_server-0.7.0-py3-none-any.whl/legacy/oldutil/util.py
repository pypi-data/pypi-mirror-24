
# TODO: no longer used

import sys

from itertools import chain
from collections import deque


def total_size(obj, verbose=False):
    """ Returns approximate memory size"""
    seen = set()

    def sizeof(o):
        if id(o) in seen:
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default=0)
        if verbose:
            print(s, type(o), repr(o))
        if isinstance(o, (tuple, list, set, frozenset, deque)):
            s += sum(map(sizeof, iter(o)))
        elif isinstance(o, dict):
            s += sum(map(sizeof, chain.from_iterable(o.items())))
        elif "__dict__" in dir(o):
            s += sum(map(sizeof, chain.from_iterable(o.__dict__.items())))
        return s

    return sizeof(obj)


def total_size_str(obj):
    s = total_size(obj)
    if 1 > s / 1000.0:
        return "{} Bytes".format(s)
    if 1 > s / 1000000.0:
        return "{} KB".format(round(s / 1000.0, 1))
    if 1 > s / 1000000000.0:
        return "{} MB".format(round(s / 1000000.0, 1))
    return "{} GB".format(round(s / 1000000000.0, 1))
