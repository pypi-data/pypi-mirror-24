
import unittest

from cheddar.web.ssphelper import parse_query


class TestSSP(unittest.TestCase):

    def parse_query(self):
        q = {
            "hoge": 1,
            "list[0][fuga]": 0,
            "list[0][hoge][piyo]": 0,
            "list[0][hoge][puyo]": 1,
        }
        parse_query(q)
