# coding: UTF-8

"""
Data table module
"""

import os
import shutil
import uuid
import atexit
import platform

from PIL import Image, ImageFont, ImageDraw


class DataTable(object):
    """
    Data table class
    """

    def __init__(self, ids):
        """
        Initialize the data with primary key column 'id'
        Param ids: list of IDs
        """
        self._table = []
        for id_ in ids:
            self._table.append([id_])
        self._cols = ["id"]
        """ Unique ID for the DataTable """
        self._table_id = str(uuid.uuid1())
        self._imgdir = "./temp" + self._table_id

    def add_row(self, row):
        """
        Add new row
        Param row: list
        """
        self._table.append(row)

    def add_row_dict(self, row):
        """
        Add new row
        Param row: dict of {column_name: column}
        """
        newrow = [""] * len(self._cols)
        for i, col in enumerate(self._cols):
            try:
                newrow[i] = row[col]
            except:
                pass
        self._table.append(newrow)

    def join(self, name, col):
        """
        Join new column
        Param col: dict of {id: column}
        """
        self._cols.append(name)
        for row in self._table:
            id_ = row[self._cols.index("id")]
            if id_ in col:
                row.append(col[id_])
            else:
                row.append("")

    def join_image(self, name, col):
        """
        Save data as a PNG image file and put it into a temporary folder.
        Join new column which include a link to the file.
        Temporary file will be automatically deleted by 'atexit'.
        Param col: dict of {id: column(bytearray or PIL.Image)}
        """
        """ If the image folder does not exist, make it. """
        if not os.path.isdir(self._imgdir):
            os.mkdir(self._imgdir)
            atexit.register(self.clear)
        if not os.path.isdir(self._imgdir + "/" + name):
            os.mkdir(self._imgdir + "/" + name)
        self._cols.append(name)
        """ Add file path to the record and save image file on temp folder. """
        for row in self._table:
            id_ = row[self._cols.index("id")]
            if id_ in col:
                filepath = self._imgdir + "/" + name + "/" + id_ + ".png"
                row.append(filepath)
                if col[id_].__class__.__name__ == "Image":
                    col[id_].save(filepath)
                elif col[id_] == "Exception: Molecule Not Found.":
                    self._render_text_img("Molecule Not Found").save(filepath)
                elif col[id_] == "Exception: Rendering Failure.":
                    self._render_text_img("Rendering Failure").save(filepath)
                else:
                    with open(filepath, 'w+b') as f:
                        f.write(col[id_])
            else:
                row.append("")

    def get_row(self, idx):
        """ Param index: index number of the row. """
        return self._table[idx]

    def get_row_dict(self, idx):
        """
        Param index: index number of the row.
        Return dict {column name: field}
        """
        dict_ = {}
        row = self._table[idx]
        for i, field in enumerate(row):
            dict_[self._cols[i]] = field
        return dict_

    def get_column(self, name):
        """ Param name: name of the columun. """
        col = []
        colindex = self._cols.index(name)
        for row in self._table:
            col.append(row[colindex])
        return col

    def get_col_header(self):
        """ Return list of column header """
        return self._cols

    def column_count(self):
        return len(self._cols)

    def row_count(self):
        return len(self._table)

    MAC_FONT_PATH = "/Library/Fonts/Tahoma.ttf"
    SIZE = (260, 260)

    def _render_text_img(self, string):
        if platform.system() == "Darwin":
            font = ImageFont.truetype(self.MAC_FONT_PATH, 16)
        else:
            font = None
        img = Image.new("RGB", self.SIZE, "#ffffff")
        draw = ImageDraw.Draw(img)
        W, H = self.SIZE
        w, h = draw.textsize(string, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), string, font=font, fill='red')
        return img

    def show(self):
        """
        Test method: show the table on the console.
        """
        print tuple(self._cols)
        for row in self._table:
            print row

    def clear(self):
        """
        Delete table contents
        Delete temporary image folder
        """
        self._table = []
        if os.path.isdir(self._imgdir):
            shutil.rmtree(self._imgdir)


def main():
    from tmp.java.sqlite import SQLiteConnection
    ids = ("T-000001", "T-00002", "T-000003")
    con = SQLiteConnection()
    structures = con.find_structures_by_ids(ids)
    print structures

if __name__ == "__main__":
    main()
