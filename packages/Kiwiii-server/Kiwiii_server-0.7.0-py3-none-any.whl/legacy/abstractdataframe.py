
# Copyright (C) 2014-2015 by Seiji Matsuoka
# All Rights Reserved.


class AbstractDataframe(object):
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

    """

    def __init__(self):
        self.df = None
        self._column = Column(self)

    def __getitem__(self, col):
        """Call column helper"""
        return self._column.instance(col)

    def row(self, idx):
        """Get row as a list. Only visible columns are shown.

        Args:
          idx (str): row index
        Returns:
          list: row
        """
        raise NotImplementedError()

    def rows_iter(self):
        """Iterate over rows. Only visible columns are shown.
        """
        raise NotImplementedError()

    def header(self):
        """Get name list of visible columns"""
        raise NotImplementedError()

    def columns(self):
        """Get name list of all columns"""
        raise NotImplementedError()

    def __len__(self):
        """Get number of rows """
        raise NotImplementedError()

    def _cell_value(self, col, idx):
        """Get value of specific cell"""
        raise NotImplementedError()

    def _set_cell_value(self, col, idx, value):
        """Set value to specific cell"""
        raise NotImplementedError()

    def _attr(self, col, name):
        """Get column attribute"""
        raise NotImplementedError()

    def _set_attr(self, col, name, value):
        """Set column attribute"""
        raise NotImplementedError()

    def _merge(self, left, right, data, cols, suffix="_"):
        """Left outer merge a dict as a new column

        Args:
            left (str): left column name
            right (str): right column name
            data (dict): dataframe to merge (list of dict)
            cols (list): columns of the dataframe
            suffix (str): if right already exists, suffix will be added
        """
        raise NotImplementedError()

    def _apply(self, x, y, func, suffix="_"):
        """Append new column with a function applied to existing column

        Args:
            x (str): column which function applies
            y (str): new column that the function is applied
            func (callable): function y=f(x)
            suffix (str): if right already exists, suffix will be added
        """
        raise NotImplementedError()

    def _sort(self, col, ascending=True):
        raise NotImplementedError()


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
