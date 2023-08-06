
import os
import unittest

from cheddar.data.pandasdataframe import Dataframe, type_hint, dumps, loads

COLS = ("name", "price", "ingredient")

LIST_OF_LIST = [
    ("sushi", 1300, "fish"),
    ("sukiyaki", 1500, "meat"),
    ("ramen", 700, "noodle")
]

DICT_OF_LIST = {
    "name": ("sushi", "sukiyaki", "ramen"),
    "price": (1300, 1500, 700),
    "ingredient": ("fish", "beef", "noodle")
}

LIST_OF_DICT = [
    {"name": "sushi", "price": 1300, "ingredient": "fish"},
    {"name": "sukiyaki", "price": 1500, "ingredient": "meat"},
    {"name": "ramen", "price": 700, "ingredient": "noodle"}
]


class TestPandasDataframe(unittest.TestCase):

    def test_build(self):
        df = Dataframe(data=LIST_OF_LIST, names=COLS)
        self.assertEqual(df.columns()[1], "price")
        self.assertEqual(df["ingredient"].name, "ingredient")
        df = Dataframe(data=DICT_OF_LIST, names=COLS)
        self.assertEqual(df.columns()[1], "price")
        self.assertEqual(df["ingredient"].name, "ingredient")
        df = Dataframe(data=LIST_OF_DICT, names=COLS)
        self.assertEqual(df.columns()[1], "price")
        self.assertEqual(df["ingredient"].name, "ingredient")
        # Safe null object
        df = Dataframe()
        self.assertEqual(len(df), 0)
        self.assertEqual(sum([1 for _ in df.rows_iter()]), 0)
        self.assertEqual(df.header(), [])

    def test_df_access(self):
        df = Dataframe(data=LIST_OF_LIST, names=COLS)
        self.assertEqual(df["name"][0], "sushi")
        self.assertEqual(sum([1 for _ in df["name"]]), 3)
        self.assertEqual(df.row(2), ["ramen", 700, "noodle"])
        self.assertEqual(len(df), 3)
        # Get and set cell value
        df["price"][2] = 800
        self.assertEqual(df["price"][2], 800)

    def test_df_attrs(self):
        df = Dataframe(data=LIST_OF_LIST, names=COLS)
        self.assertEqual(df.header(), ["name", "price", "ingredient"])
        # Get and set attribute
        df["price"].type = int
        self.assertEqual(df["price"].type, int)
        # Set visible=False to hide columns
        df["price"].visible = False
        self.assertEqual(df.header(), ["name", "ingredient"])
        self.assertEqual(df.columns(), ["name", "price", "ingredient"])
        self.assertEqual(df.row(2), ["ramen", "noodle"])
        self.assertTrue(all([len(row) == 2 for row in df.rows_iter()]))

    def test_merge(self):
        df = Dataframe(data=DICT_OF_LIST, names=COLS)
        order = {
            "namae": ("sushi", "sukiyaki", "ramen"),
            "order1": (1, 2, 3),
            "order2": (4, 1, 2)
        }
        df["name"].merge("namae", order, ("namae", "order1", "order2"))
        self.assertEqual(df["order1"][2], 3)
        self.assertEqual(df["order1"].visible, True)
        df["name"].merge("namae", order, ("namae", "order1", "order2"))
        self.assertEqual(df["order2_"][1], 1)

    def test_apply(self):
        df = Dataframe(data=DICT_OF_LIST, names=COLS)
        df["price"].apply("price_twice", lambda x: x * 2)
        self.assertEqual(df["price_twice"][2], 1400)
        self.assertEqual(df["price_twice"].visible, True)
        df["price"].apply("price_twice", lambda x: x * 2)
        self.assertEqual(df["price_twice_"][2], 1400)

    def test_dol(self):
        df = Dataframe(data=DICT_OF_LIST, names=COLS)
        self.assertEqual(df.dict_of_list()["ingredient"][2], "noodle")

    @unittest.skip("Deprecated")
    def test_type_hint(self):
        self.assertEqual(type_hint([1, 2, 3]), "int")
        self.assertEqual(type_hint([1, 2.2, 3]), "float")
        self.assertEqual(type_hint([1, "hoge", 2.34]), "text")
        self.assertEqual(type_hint(["fuga", "hoge", object]), "object")
        self.assertEqual(type_hint([1, 2, None]), "int")
        self.assertEqual(type_hint(["fuga", None, "hoge"]), "text")
        self.assertEqual(type_hint([None, None, None]), None)

    def test_dump(self):
        df = Dataframe(data=DICT_OF_LIST, names=COLS)
        d = dumps(df)
        resumed = loads(d)
        self.assertEqual(len(resumed), len(df))
        self.assertEqual(resumed.attr_table.shape[0], df.attr_table.shape[0])
