# coding: UTF-8

import os
import shutil
import uuid

import pandas

from xlsxwriter.workbook import Workbook
from tmp import image


class DataTable(object):
    """Pandas table class

    Attribute:
        df: pandas dataframe
    """

    def __init__(self):
        self.df = None
        self._tmpdir = "./.tmp" + str(uuid.uuid1())

    def init_df(self, data=None, columns=None):
        """Initialize dataframe

        Args:
          data: [col1, col2, col3, ...]
          columns: [col1, col2, col3, ...] (optional)
        """
        self.df = pandas.DataFrame(data=data, columns=columns)

    def dict_(self):
        """Return dict type data of the table

        Returns:
          {0: {col1: val, col2: val, ...}, 1: {}, ...}
        """
        return self.df.drop("Mol", 1).T.to_dict()

    def dict_inverse(self):
        """Return inverse dict type data of the table

        Returns:
          {col1: {0: val, 1: val, ...}, col2: {}, ...}
        """
        return self.df.drop("Mol", 1).to_dict()

    def append_row(self, row):
        """
        Args:
          row: {col_name1: value1, col_name2: value2, ...}
        """
        self.df = self.df.append(row, ignore_index=True)

    def join(self, left, right, data):
        """Left join new column

        Args:
          left: string
          right: string
          data: {key: value, ...}
        """
        right_col = pandas.Series(data, name=right)
        self.df = self.df.join(right_col, on=left, rsuffix="_")

    def calc(self, original, func, applied):
        """Add new column which applies a function to an existing column
        (similar to python map function)

        Args:
          original: original column name
          func: function
          applied: new column name
        """
        self.df[applied] = self.df[original].apply(func)

    def column_names(self):
        """
        Returns: list of column names
        """
        return list(self.df.drop("Mol", 1).columns.values)

    def row(self, idx):
        """
        Args:
          idx: index of the row
        Returns:
          list of row elements
        """
        return list(self.df.ix[idx])

    def column(self, name):
        """
        Args:
          name: column name
        Returns:
          list of column elements
        """
        return list(self.df[name])

    def row_count(self):
        """
        Returns: number of rows
        """
        return self.df.shape[0]

    def column_count(self):
        """
        Returns: number of columns
        """
        return self.df.shape[1]

    def export_xlsx(self, path):
        """Export to Microsoft Excel worksheet(.xlsx)

        Args:
          path: file to be saved
        """
        os.mkdir(self._tmpdir)
        dict_ = self.dict_inverse()
        cell_height = 220
        img_cell_option = {
            'x_offset': 10, 'y_offset': 10,
            'x_scale': 1.4, 'y_scale': 1.4, 'anchor': 2
        }  # 1.4 is empirical
        workbook = Workbook(path)
        format_ = workbook.add_format({"align": "center", "valign": "vcenter"})
        worksheet = workbook.add_worksheet("sheet1")
        worksheet.set_default_row(cell_height)
        worksheet.set_row(0, 20)
        for i, col in enumerate(self.column_names()):
            worksheet.write(0, i, col, format_)
            column_width_en = 16
            for j, val in dict_[col].items():
                if isinstance(val, bytearray):
                    tup = (self._tmpdir, col, str(j))
                    filepath = "%s/%s_%s.png" % tup
                    resized = image.resize_by_height(val, cell_height - 20)
                    width, height = image.get_size(resized)
                    with open(filepath, 'wb') as f:
                        f.write(resized)
                    if width > column_width_en * 5:
                        column_width_en = width / 5 + 2
                    worksheet.insert_image(j + 1, i, filepath, img_cell_option)
                else:
                    worksheet.write(j + 1, i, val, format_)
            worksheet.set_column(i, i, column_width_en)
        workbook.close()
        shutil.rmtree(self._tmpdir)
