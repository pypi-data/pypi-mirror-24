
import math
import time


NUMBER = 1000000


def check_time(func, name=None):
    start1 = time.time()
    result = func()
    print("<{}> {} sec, Result:{}".format(
        name, round(time.time() - start1, 4), result))


def test1(i):
    if i % 2 == 0:
        return 1
    else:
        return 0


def test1a(i):
    if i % 2 == 0:
        return 1
    return 0


def test2():
    for i in range(NUMBER):
        if i % 2 == 0:
            yield 1
        else:
            yield 0


def test2a():
    for i in range(NUMBER):
        if i % 2 == 0:
            yield 1
        yield 0


def test2b():
    case = {0: 1, 1: 0}
    for i in range(NUMBER):
        yield case[i % 2]


def test2c():
    case = {0: 1}
    for i in range(NUMBER):
        try:
            result = case[i % 2]
        except KeyError:
            result = 0
        yield result


def test2d():
    i = 0
    while 1:
        try:
            if i == NUMBER:
                raise StopIteration
            if i % 2 == 0:
                yield 1
            else:
                yield 0
            i += 1
        except StopIteration:
            break


def test2e():
    i = 0
    try:
        while 1:
            if i == NUMBER:
                raise StopIteration
            if i % 2 == 0:
                yield 1
            else:
                yield 0
            i += 1
    except StopIteration:
        pass


def test3():
    for i in range(NUMBER):
        if i % 3 == 0:
            yield 1
        elif i % 3 == 1:
            yield 0.5
        else:
            yield 0


def test3a():
    case = {0: 1, 1: 0.5, 2: 0}
    for i in range(NUMBER):
        yield case[i % 3]


import multiprocessing as mp
PROCESSES = 4


def test4_task(q, range_):
    q.put(sum(map(test1, range(*range_))))


def test4():
    queue = mp.Queue()
    task_size = math.ceil(NUMBER / PROCESSES)
    ranges = []
    for i in range(PROCESSES):
        ranges.append((i * task_size, min([(i + 1) * task_size, NUMBER])))
    processes = [mp.Process(group=None, target=test4_task, args=(queue, range_))
                 for range_ in ranges]
    for process in processes:
        process.start()
    result = []
    for process in processes:
        result.append(queue.get())
        process.join()
    return sum(result)


def test4a():
    with mp.Pool(PROCESSES) as pool:
        imap_it = pool.imap(test1, range(NUMBER))
        result = sum(imap_it)
    return result

"""
from cheddar.chem.v2000supplier import _sdfile_to_ctab
from cheddar.chem.v2000supplier import ctab_to_compound
from cheddar.chem.model.graphmol import build
from cheddar.util.itertools import chunk


def test_sdf_task(x):
    return build(ctab_to_compound(x))


def test_sdf_task2(x):
    m = build(ctab_to_compound(x))
    return m.mw()


def test_sdf_task3(iterable):
    return [build(ctab_to_compound(i)) for i in iterable]


def test_sdf():
    it = _sdfile_to_ctab("./datasource/DrugBank_FDA_Approved.sdf")
    return sum(i.mw() for i in map(test_sdf_task, it))


def test_sdf2_1():
    it = _sdfile_to_ctab("./datasource/DrugBank_FDA_Approved.sdf")
    with mp.Pool(PROCESSES) as pool:
        result = sum(i.mw() for i in pool.imap(test_sdf_task, it))
    return result


def test_sdf2_2():
    it = _sdfile_to_ctab("./datasource/DrugBank_FDA_Approved.sdf")
    with mp.Pool(PROCESSES) as pool:
        result = sum(pool.imap(test_sdf_task2, it))
    return result


def test_sdf2_3():
    it = chunk(
        _sdfile_to_ctab("./datasource/DrugBank_FDA_Approved.sdf"), 50)
    with mp.Pool(PROCESSES) as pool:
        imap_it = pool.imap(test_sdf_task3, it)
        result = sum(sum(j.mw() for j in i) for i in imap_it)
    return result
"""

def test5(i):
    if i == 10000:
        return 0
    else:
        return i / 10000


def test5a(i):
    try:
        return i / 10000
    except ZeroDivisionError:
        return 0


ls = (1, 45, 23, 124, 54, 4, 13, 46, 24, 12, 1, 45, 23, 124, 54, 4,
      13, 46, 24, 12, 1, 45, 23, 124, 54, 4, 13, 46, 24, 12, 1, 45,
      23, 124, 54, 4, 13, 46, 24, 12)


def test_minmax1():
    s = sorted(ls)
    return s[0] + s[-1]


def test_minmax2():
    max_ = max(ls)
    min_ = min(ls)
    return max_ + min_


def test_minmax3():
    max_, min_ = (max(ls), min(ls))
    return max_ + min_


# check_time(lambda: sum(test1(x) for x in range(NUMBER)), "test1")
# check_time(lambda: sum(test1a(x) for x in range(NUMBER)), "test1a")
# check_time(lambda: sum(test5(x) for x in range(NUMBER)), "test5")
# check_time(lambda: sum(test5a(x) for x in range(NUMBER)), "test5a")
# check_time(lambda: sum(test2()), "test2")
# check_time(lambda: sum(test2a()), "test2a")
# check_time(lambda: sum(test2b()), "test2b")
# check_time(lambda: sum(test2c()), "test2c")
# check_time(lambda: sum(test2d()), "test2d")
# check_time(lambda: sum(map(test1, range(NUMBER))), "test2c")
# check_time(lambda: sum(test3()), "test3")
# check_time(lambda: sum(test3a()), "test3a")
# check_time(test4, "test4")
# check_time(test4, "test4a")

# check_time(test_sdf, "test_sdf_new")
# check_time(test_sdf2_1, "test_sdf2_1")
# check_time(test_sdf2_2, "test_sdf2_2")
# check_time(test_sdf2_3, "test_sdf2_3")


# check_time(lambda: sum(test_minmax1() for _ in range(NUMBER)), "test_minmax1")
# check_time(lambda: sum(test_minmax2() for _ in range(NUMBER)), "test_minmax2")
# check_time(lambda: sum(test_minmax3() for _ in range(NUMBER)), "test_minmax3")

import numpy as np


def test_from_list(size):
    ls = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(i + j)
        ls.append(row)
    res = np.array(ls)
    return res


def test_empty_replace(size):
    res = np.empty((size, size))
    for i in range(size):
        for j in range(size):
            res[i][j] = i + j
    return res

check_time(lambda: np.sum(test_from_list(1000)), "test_from_list")
check_time(lambda: np.sum(test_empty_replace(1000)), "test_empty_replace")
