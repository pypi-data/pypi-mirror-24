# Copyright (C) 2014-2015 by Seiji Matsuoka
# All Rights Reserved.

import pickle

from cheddar.data.abstractdataframe import AbstractDataframe
from cheddar.util import util


class Dataframe(AbstractDataframe):
    """Table structure dataframe

    * dataframe construction

        The dataframe supports following input format.

        * dict of list

        >>> df = Dataframe(data={
        ...     "name": ("sushi", "sukiyaki", "ramen"),
        ...     "price": (1300, 1500, 700),
        ...     "ingredient": ("fish", "beef", "noodle")
        ... }, names=("name", "price", "ingredient"))

        * list of dict

        >>> df = Dataframe(data=[
        ...     {"name": "sushi", "price": 1300, "ingredient": "fish"},
        ...     {"name": "sukiyaki", "price": 1500, "ingredient": "meat"},
        ...     {"name": "ramen", "price": 700, "ingredient": "noodle"}
        ... ], names=("name", "price", "ingredient"))

        "list of list" is not supported.
        Augment 'names' is not required but is recommended to set
        due to specify the order of columns to be displayed.
    """

    def __init__(self, data=None, names=()):
        super().__init__()
        self.df = {}
        if isinstance(data, list):  # list of dict
            for d in data:
                for k, v in d.items():
                    if k in self.df:
                        self.df[k].append(v)
                    else:
                        self.df[k] = [v]
        elif isinstance(data, dict):  # dict of list
            for k, v in data.items():
                self.df[k] = list(v)
        elif data is None:
            self.df = {n: [] for n in names}
        else:
            raise TypeError("invalid source format")
        self.cols = list(names)
        self.attrs = {}
        for n in names:
            self.attrs[n] = {"name": n, "visible": True, "type": object}

    def columns(self):
        return self.cols

    def header(self):
        return tuple(col for col in self.columns() if self[col].visible)

    def row(self, idx):
        return tuple(self.df[col][idx] for col in self.header())

    def rows_iter(self):
        for row in zip(*[self.df[col] for col in self.header()]):
            yield tuple(row)

    def dict_of_list(self):
        return self.df

    def total_size(self):
        return util.total_size(self)

    def __len__(self):
        return max([len(self.df[col]) for col in self.columns()], default=0)

    def _merge(self, L_key, R_key, data, cols, suffixes=("", "_")):
        R_cols = list(cols[:])
        for i, r in enumerate(R_cols):
            if r in self.columns():  # Avoid col name collision
                newLkey = suffixes[0] + r
                self.df[newLkey] = self.df.pop(r)
                self.columns()[self.columns().index(r)] = newLkey
                newRkey = r + suffixes[1]
                data[newRkey] = data.pop(r)
                R_cols[i] = newRkey
                self.df[newRkey] = []
                self.columns().append(newRkey)
                if r == R_key:
                    R_key = newRkey
            else:
                self.df[r] = []
                self.columns().append(r)
            self.attrs[r] = {"name": r, "visible": True, "type": object}
        for L in self.df[L_key]:
            R = data[R_key]
            if L in R:
                for r in R_cols:
                    self.df[r].append(data[r][R.index(L)])
            else:
                for r in R_cols:
                    self.df[r].append('-')

    def _apply(self, x, y, func, rsuffix="_"):
        if y in self.columns():
            new_y = y + rsuffix
        else:
            new_y = y
        self.df[new_y] = list(map(func, self.df[x]))
        self.columns().append(new_y)
        self.attrs[new_y] = {"visible": True, "type": object}

    def _sort(self, ascending=True):
        # TODO: not yet implemented
        self.__dict__["_pdf"].df[self._col] = self._pdf.sort(
            columns=self._col)

    def _cell_value(self, col, idx):
        """Get value of specific col and row"""
        return self.df[col][idx]

    def _set_cell_value(self, col, idx, value):
        """Set value to specific col and row"""
        self.df[col][idx] = value

    def _attr(self, col, attr):
        """Get column attribute"""
        return self.attrs[col][attr]

    def _set_attr(self, col, attr, value):
        """Set column attribute"""
        self.attrs[col][attr] = value


def dumps(df):
    """ Pickle dataframe object and save it on the file.
    """
    # Dataframe itself is not picklable because of recursion in Column call
    contents = {"df": df.df, "cols": df.cols,
                "attrs": df.attrs}
    return pickle.dumps(contents)


def loads(dump):
    """ Load stored data file and unpickle the dataframe object.
    """
    contents = pickle.loads(dump)
    df = Dataframe()
    df.df = contents["df"]
    df.cols = contents["cols"]
    df.attrs = contents["attrs"]
    return df
