
import os
import unittest

# from cheddar.data.csvsupplier import csv_supplier, scan, ParseOption
# from cheddar.test.data.datafileprovider import FILE_DIR


@unittest.skip("Deprecated")
class TestCsvParser(unittest.TestCase):

    def _path(self):
        return os.path.join(FILE_DIR, "test.csv")

    def _path2(self):
        return os.path.join(FILE_DIR, "assay1_tab_sep.txt")

    def test_parse(self):
        sup = csv_supplier(self._path())
        result = {"index": "1", "hoge": "1.23", "fuga": "3.5", "12": "hoge"}
        self.assertEqual(next(sup), result)

    def test_parse_tsv(self):
        opt = ParseOption()
        opt.delimiter = "\t"
        fields, count = scan(self._path2(), opt)
        sup = csv_supplier(self._path2(), opt)
        self.assertEqual(sum(1 for _ in sup), count)
        self.assertEqual(len(fields), 5)
