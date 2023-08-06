
import sqlite3


class Connection(object):

    def __init__(self, path):
        self._con = sqlite3.connect(path)
        self._con.row_factory = sqlite3.Row

    def tables(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        return [row["name"] for row in self._con.execute(sql)]

    def columns(self, table):
        sql = "PRAGMA table_info({})".format(table)
        return [row["name"] for row in self._con.execute(sql)]

    def rows_iter(self, tables, orderby=None):
        """Iterate over rows of tables"""
        if orderby is None:
            od = ""
        else:
            od = " ORDER BY " + ", ".join(orderby)
        for table in tables:
            sql = "SELECT * FROM {}{}".format(table, od)
            for row in self._con.execute(sql):
                yield row

    def rows_count(self, tables):
        """Returns number of records of tables"""
        cnts = []
        for table in tables:
            sql = "SELECT count(*) FROM {}".format(table)
            cnts.append(self._con.execute(sql).fetchone()["count(*)"])
        return sum(cnts)

    def find_iter(self, key, value, tables, condition="="):
        """find records and return result generator"""
        if condition == "IN":
            ph = "({})".format(", ".join(["?" for _ in value]))
            where = " WHERE {} in{}".format(key, ph)
            val = value
        else:
            where = " WHERE {} {} ?".format(key, condition)
            val = (value, )
        for table in tables:
            sql = "SELECT * FROM {}{}".format(table, where)
            for row in self._con.execute(sql, val):
                yield row

    def find_first(self, key, value, tables, null_record=False):
        """find records and return first one

        Returns:
            dict: result rows
            None: if nothing is found
        """
        for table in tables:
            sql = "SELECT * FROM {} WHERE {}=?".format(table, key)
            res = self._con.execute(sql, (value,)).fetchone()
            if res is not None:
                return res
        if null_record:
            return self._null_response_record(key, value, table)

    def _null_response_record(self, key, value, table):
        """ Return the query with null record """
        # TODO: need refactoring
        import pickle
        from chemex.draw.svg import SVG
        from chemex.model.graphmol import Compound
        svg = SVG(Compound())
        res = {"_mol": pickle.dumps(Compound()), "_structure": svg.contents(),
               "_mw": 0, "_mw_wo_sw": 0}
        cols = {c: "" for c in self.columns(table) if not c.startswith("_")}
        cols[key] = value
        res.update(cols)
        return res
