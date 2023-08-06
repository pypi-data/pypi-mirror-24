
# TODO: no longer used

import itertools


def chunk(iterable, size):
    """
    chunk('ABCDEFG', 3) --> ABC DEF G
    """
    # TODO: only used in gui.mainwindow(deprecated)
    iterator = iter(iterable)
    while size:
        result = []
        try:
            for i in range(size):
                elem = next(iterator)
                result.append(elem)
            yield tuple(result)
        except StopIteration:
            if result:
                yield tuple(result)
            return


def chunk_truncate(iterable, size):
    """
    chunk_truncate('ABCDEFG', 3) --> ABC DEF
    """
    # TODO: only used in kekulize(deprecated)
    args = [iter(iterable)] * size
    return zip(*args)


def chunk_fill(iterable, size, fillvalue=None):
    """
    chunk_fill('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    # TODO: not used
    args = [iter(iterable)] * size
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def consecutive(iterable, n):
    """
    consective('ABCDEF', 3) --> ABC BCD CDE DEF
    consective(itertools.cycle(iter, n)) to get looped sequence
    """
    iterators = itertools.tee(iterable, n)
    for i, it in enumerate(iterators):
        for j in range(i):
            next(it, None)
    return zip(*iterators)
