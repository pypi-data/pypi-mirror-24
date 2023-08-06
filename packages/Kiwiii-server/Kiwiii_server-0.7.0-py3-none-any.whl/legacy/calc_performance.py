from cheddar.util.profile import profile

import numpy as np
import numexpr as ne
from cheddar.chem.cython_nonzero import nonzero as nonzero_c


@profile
def example(arr1, arr2):
    result = []
    for i, e1 in enumerate(arr1):
        for j, e2 in enumerate(arr2):
            if e1 == e2:
                result.append((i, j))
    return result


@profile
def example_numpy(arr1, arr2):
    c1 = np.array(arr1, dtype=int)
    c2 = np.array(arr2, dtype=int)
    c1 = c1[:, np.newaxis]
    m = c2 == c1
    result = []
    for p in zip(*np.nonzero(m)):
        result.append(p)
    return result


@profile
def example_numexpr(arr1, arr2):
    c1 = np.array(arr1, dtype=int)
    c2 = np.array(arr2, dtype=int)
    c1 = c1[:, np.newaxis]
    m = ne.evaluate("c2 == c1")
    result = []
    for p in zip(*np.nonzero(m)):
        result.append(p)
    return result


@profile
def example_cython(arr1, arr2):
    return nonzero_c(arr1, arr2)


if __name__ == "__main__":
    arr1 = [i for i in range(1000000) if i % 17 == 0]
    arr2 = [i for i in range(1000000) if i % 37 == 0]
    print(len(example_cython(arr1, arr2)))
