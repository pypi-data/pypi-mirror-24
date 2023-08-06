
from pandas import DataFrame, Series


class Table(object):
    """
    Pandas table class
    """

    def __init__(self, cols=None):
        """
        Initialize the data
        Param cols: [col1, col2, col3, ...]
        """
        self._df = DataFrame(columns=cols)

    def get_dataframe(self):
        """
        Return dataframe
        """
        return self._df

    def append_row(self, row):
        """
        Add new row
        Param row: {col_name: value, ...}
        """
        self._df = self._df.append(row, ignore_index=True)

    def join(self, key, value, dict_):
        """
        Join new column
        Param key: string
        Param value: string
        Param dict_: {key: value, ...}
        """
        new_col = Series(dict_, name=value)
        self._df = self._df.join(new_col, on=key)


def main():
    cols = ["name", "age", "hoge", "hunya"]
    table = Table(cols)
    dict1 = {"name": "Bob", "age": 17, "hoge": "hogehoge"}
    dict2 = {"name": "Alice", "age": 19, "hoge": "hogefoge"}
    dict3 = {"name": "Mary", "age": 24, "hoge": "hogefoge"}
    table.append_row(dict1)
    table.append_row(dict2)
    table.append_row(dict3)
    table.join("name", "sex", {"Bob": "F", "Alice": "M"})
    print table.get_dataframe()

    #names = ['Bob', 'Jessica', 'Mary', 'John', 'Mel']
    #births = [968, 155, 77, 578, 973]
    #BabyDataSet = zip(names, births)

    #df = DataFrame(data=BabyDataSet, columns=['Names', 'Births'])
    #print df

    #print df.Names.ix[0]
    #with open("hogehoge.png", "wb") as image_file:
    #    image_file.write(df.Birth.ix[0])


if __name__ == "__main__":
    main()
