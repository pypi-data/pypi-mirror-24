
"""
SQLite database connection module
"""

import traceback
import sqlite3

import exception
from tmp import settings


class Connection(object):
    """SQLite database connection class

    Attribute:
      db_path: sqlite3 db path
      table: sqlite3 table
      primary_key: primary_key
      mol_col: molfile string column
    """

    def __init__(self, table=None):
        self.db_path = settings.DEFAULT_DB_PATH
        self.table = table
        self.key = settings.DB_TABLE_MAPPING[
            "default_primary_key"]
        self.mol_col = settings.DB_TABLE_MAPPING[
            "default_molecule_col"]

    def find_structures_by_ids(self, ids):
        return self.find_by_ids(ids, self.mol_col)

    def find_by_ids(self, ids, col):
        """Find records by IDs

        Args:
          ids: list of ID string
          col: column
        Returns:
          {id1: record1, id2: record2, ...}
        Raises:
          SQLiteConnectionError
        """
        sanitizer = lambda str_: "\'{}\'".format(str_.replace("\'", "\'\'"))
        id_query = "({})".format(", ".join(map(sanitizer, ids)))
        try:
            con = sqlite3.connect(self.db_path)
        except sqlite3.DatabaseError:
            print traceback.format_exc()
            raise exception.SQLiteConnectionError
        try:
            cursor = con.cursor()
            tup = (self.key, col, self.table, self.key, id_query)
            cursor.execute("select {}, {} from {} where {} in {}".format(*tup))
            records = dict(cursor.fetchall())
            cursor.close()
        except sqlite3.OperationalError:
            print traceback.format_exc()
            return None
        return {id_: records.get(id_) for id_ in ids}

    def findfirst(self, query):
        """
        Simply execute SQL.
        param query: SQL query string
        return dict of {column name: field}
        """
        try:
            con = sqlite3.connect(self.db_path)
        except sqlite3.DatabaseError:
            print traceback.format_exc()
            raise exception.SQLiteConnectionError
        con.row_factory = _dict_factory
        try:
            cursor = con.cursor()
            cursor.execute(query)
            record = cursor.fetchone()
            cursor.close()
        except sqlite3.OperationalError:
            print traceback.format_exc()
            return None
        return record


def _dict_factory(cursor, row):
    """ Generate dict of {column name: value} (override row_factory) """
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


def main():
    pass

if __name__ == "__main__":
    main()
