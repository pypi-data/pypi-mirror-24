# Copyright (C) 2014-2015 by Seiji Matsuoka
# All Rights Reserved.

import pickle
from cheddar.util import util


class Dataframe(object):
    """Dataframe base class

    * Dataframe structure

        +-----+-----+-------------+-------------+-------------+
        |           |                 column                  |
        +           +-------------+-------------+-------------+
        |           |name         |price        |ingredient   |
        +-----+-----+-------------+-------------+-------------+
        |attribute  |visible=True |visible=True |visible=True |
        |           |type=str     |type=int     |type=str     |
        +-----+-----+-------------+-------------+-------------+
        |     |0    |sushi        |1300         |fish         |
        +     +-----+-------------+-------------+-------------+
        |row  |1    |sukiyaki     |1500         |beef         |
        +     +-----+-------------+-------------+-------------+
        |     |2    |ramen        |700          |noodle       |
        +-----+-----+-------------+-------------+-------------+

    * Get a record

        >>> df["price"][1]
        1500

    * Get a column

        >>> [i for i in df["ingredient"]]
        ["fish", "beef", "noodle"]

    * Get a row

        >>> df.row(0)
        ["sushi", 1300, "fish"]

    * Iterate over rows

        >>> for row in df.rows_iter():
        ...     print(row)
        ["sushi", 1300, "fish"]
        ["sukiyaki", 1500, "beef"]
        ["ramen", 700, "noodle"]

    * Count rows

        >>> len(df)
        3

    * Show column header

        >>> df.header()
        ["name", "price", "ingredient"]

    * Hide column

        >>> df["price"].visible = False
        >>> df.header()
        ["name", "ingredient"]
        >>> df.row(0)
        ["sushi", "fish"]
        >>> for row in df.rows_iter():
        ...     print(row)
        ["sushi", "fish"]
        ["sukiyaki", "beef"]
        ["ramen", "noodle"]

    * Get and set column attribute

        >>> df["price"].type = int
        >>> df["price"].type
        int

        Phrase 'apply', 'merge', 'sort' are preserved for method.
        These should not be used as attribute name.

    * merge dataframes

        >>> order = {
        >>>     "namae": ("sushi", "sukiyaki", "ramen"),
        >>>     "order1": (1, 2, 3),
        >>>     "order2": (4, 1, 2)
        >>> }
        >>> df["name"].merge("namae", order,
        >>>                  ("namae", "order1", "order2"))
        >>> df.header()
        ["name", "price", "ingredient", "order1", "order2"]
        >>> for row in df.rows_iter():
        ...     print(row)
        ["sushi", 1300, "fish", 1, 4]
        ["sukiyaki", 1500, "beef", 2, 1]
        ["ramen", 700, "noodle", 3, 2]

    * apply function to the column

        >>> df["price"].apply("price_twice", lambda x: x * 2)
        >>> df.header()
        ["name", "price", "ingredient", "price_twice"]
        >>> for row in df.rows_iter():
        ...     print(row)
        ["sushi", 1300, "fish", 2600]
        ["sukiyaki", 1500, "beef", 3000]
        ["ramen", 700, "noodle", 1400]

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
        self._column = Column(self)
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
            if n not in self.df:  # fill blank columns
                self.df[n] = [""] * len(self)

    def __getitem__(self, col):
        """Call column helper"""
        return self._column.instance(col)

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
        return pickle.loads(pickle.dumps(self.df))

    def list_of_dict(self):
        container = []
        it = {k: iter(v) for k, v in self.df.items()}
        while 1:
            try:
                container.append({k: next(v) for k, v in it.items()})
            except StopIteration:
                break
        return container

    def __len__(self):
        if not len(self.cols):
            return 0
        return len(self.df[self.cols[0]])

    def _merge(self, L_key, R_key, data, cols, suffixes=("", "_")):
        """Left outer merge a dict as a new column

        Args:
            left (str): left column name
            right (str): right column name
            data (dict): dataframe to merge (list of dict)
            cols (list): columns of the dataframe
            suffix (str): if right already exists, suffix will be added
        """
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
        """Append new column with a function applied to existing column

        Args:
            x (str): column which function applies
            y (str): new column that the function is applied
            func (callable): function y=f(x)
            suffix (str): if right already exists, suffix will be added
        """
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


class Column(object):
    """Helper class for simple indexing."""
    def __init__(self, df):
        self.__dict__["_df"] = df

    def instance(self, col):
        self.__dict__["_col"] = col
        # TODO: pandas specific "index.get_loc"
        # self.__dict__["loc"] = self._df.attr_table.index.get_loc(col)
        return self

    def __getitem__(self, key):
        return self._df._cell_value(self._col, key)

    def __setitem__(self, key, value):
        self.__dict__["_df"]._set_cell_value(self._col, key, value)

    def __getattr__(self, name):
        return self._df._attr(self._col, name)

    def __setattr__(self, name, value):
        self.__dict__["_df"]._set_attr(self._col, name, value)

    def __iter__(self):
        self.__dict__["_idx"] = 0
        return self

    def __next__(self):
        if self._idx >= len(self._df):
            raise StopIteration
        result = self._df._cell_value(self._col, self._idx)
        self.__dict__["_idx"] += 1
        return result

    def merge(self, *args, **kwargs):
        self._df._merge(self._col, *args, **kwargs)

    def apply(self, *args, **kwargs):
        self._df._apply(self._col, *args, **kwargs)

    def sort(self, *args, **kwargs):
        self._df._sort(self._col, *args, **kwargs)


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
