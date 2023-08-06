# Copyright (C) 2014-2015 by Seiji Matsuoka
# All Rights Reserved.

import pickle
import pandas as pd

from cheddar.data.abstractdataframe import AbstractDataframe


# Deprecated: use ListDataframe.


class Dataframe(AbstractDataframe):
    """Table structure dataframe

    * dataframe construction

        The dataframe supports following input format which are also acceptable
        in Pandas.

        *　list of list

        >>> df = Dataframe(data=[
        ...     ("sushi", 1300, "fish"),
        ...     ("sukiyaki", 1500, "meat"),
        ...     ("ramen", 700, "noodle")
        ... ], names=("name", "price", "ingredient"))

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

        Augment 'names' is not required for dict of list and list of dict
        but is recommended to set due to specify the order of columns
        to be displayed.
    """

    def __init__(self, data=None, names=()):
        super().__init__()
        self.df = pd.DataFrame(data=data, columns=names, dtype=object)
        self.df = self.df.fillna("-")
        attrs = {"name": names, "visible": [True] * len(names),
                 "type": [object] * len(names)}
        self.attr_table = pd.DataFrame(data=attrs, index=names)

    def row(self, idx):
        return list(self.df[self.header()].iloc[idx])

    def rows_iter(self):
        visible_df = self.df[self.header()]
        for _, row in visible_df.iterrows():
            yield list(row)

    def header(self):
        return list(self.attr_table["name"][self.attr_table["visible"]])

    def columns(self):
        return list(self.attr_table["name"])

    def dict_of_list(self):
        res = {}
        for h in self.header():
            res[h] = list(self[h])
        return res

    def total_size(self):
        return self.df.memory_usage().sum()

    def __len__(self):
        return self.df.shape[0]

    def _merge(self, left_key, rkey, rdata, rnames, suffixes=("", "_")):
        right_df = pd.DataFrame(data=rdata, columns=rnames)
        self.df = pd.merge(self.df, right_df,
                           left_on=left_key, right_on=rkey, suffixes=suffixes)
        del self.df[rkey]
        added_cols_num = right_df.shape[1] - 1
        new_rnames = self.df.columns[-added_cols_num:]
        for nr in new_rnames:
            self.attr_table.loc[nr] = pd.Series(
                {"name": nr, "visible": True, "type": object}, name=nr)
        self.df = self.df.fillna("N/A")

    def _apply(self, x, y, func, rsuffix="_"):
        if y in self.df.columns:
            new_y = y + rsuffix
        else:
            new_y = y
        self.df[new_y] = self.df[x].apply(func)
        self.attr_table.loc[new_y] = pd.Series(
            {"name": new_y, "visible": True, "type": object}, name=new_y)

    def _sort(self, ascending=True):
        # TODO: not yet implemented
        self.__dict__["_pdf"].df[self._col] = self._pdf.sort(
            columns=self._col)

    def _cell_value(self, col, idx):
        """Get value of specific col and row"""
        return self.df.loc[idx, col]

    def _set_cell_value(self, col, idx, value):
        """Set value to specific col and row"""
        self.df.loc[idx, col] = value

    def _attr(self, col, name):
        """Get column attribute"""
        return self.attr_table.loc[col, name]

    def _set_attr(self, col, name, value):
        """Set column attribute"""
        self.attr_table.loc[col, name] = value


def dumps(df):
    """ Pickle dataframe object and save it on the file.
    """
    contents = {"data": df.df.to_dict(orient="list"),
                "attr": df.attr_table.to_dict(orient="list")}
    return pickle.dumps(contents)


def loads(dump):
    """ Load stored data file and unpickle the dataframe object.
    """
    contents = pickle.loads(dump)
    df = Dataframe()
    df.attr_table = pd.DataFrame(data=contents["attr"],
                                 index=contents["attr"]["name"])
    df.df = pd.DataFrame(data=contents["data"], columns=df.attr_table["name"],
                         dtype=object)
    return df


def type_hint(data):
    """[Deprecated] Infer datatype of sequence

    Args:
      data (iterable): data

    Returns:
      Suitable datatype
      Mixed array will be upcasted (int => float => text => object)
      Sequence of None will result None

    """
    func = iter((lambda x: ""[x], lambda x: float(x)))
    f = next(func)
    r = None
    for e in data:
        if pd.isnull(e):
            # ""[None], float(None)
            continue
        while 1:
            try:
                f(e)
            except IndexError:
                # ""[1]
                r = "int"
                break
            except TypeError:
                try:
                    f = next(func)
                except StopIteration:
                    # float(object)
                    return "object"
                # ""[1.2], ""["hoge"], ""[object]
                r = "float"
            except ValueError:
                # float("hoge")
                r = "text"
                break
            else:
                # float(1.2)
                break
    return r
