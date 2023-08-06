
import pandas


def new(header=None, contents=None):
    return pandas.DataFrame()


#deprecated
def new_with_column(name, list_):
    df = pandas.DataFrame()
    df[name] = list_
    return df


def append_row(df, dict_):
    return df.append(dict_, ignore_index=True)


def col_count(df):
    return df.shape[1]


def row_count(df):
    return df.shape[0]


def col_header(df):
    return list(df.columns.values)


def row(df, index):
    return df.ix[index]