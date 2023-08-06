# Copyright (C) 2014-2015 by Seiji Matsuoka
# All Rights Reserved.

import pickle

import networkx as nx

from cheddar.data.dataframe import Dataframe as BaseDataframe


class Dataframe(BaseDataframe):
    """Table structure dataframe for web app
    """

    def __init__(self, data=None, names=()):
        super().__init__(data, names)
        self.expires = None
        self.graph = nx.Graph()


def dumps(df):
    """ Pickle dataframe object and save it on the file.
    """
    # Dataframe itself is not picklable because of recursion in Column call
    contents = {"df": df.df, "cols": df.cols,
                "attrs": df.attrs, "graph": df.graph}
    return pickle.dumps(contents, protocol=4)


def loads(dump):
    """ Load stored data file and unpickle the dataframe object.
    """
    contents = pickle.loads(dump)
    df = Dataframe()
    df.df = contents["df"]
    df.cols = contents["cols"]
    df.attrs = contents["attrs"]
    df.graph = contents["graph"]
    return df
