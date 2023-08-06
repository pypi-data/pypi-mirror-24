
from PySide import QtGui, QtCore

from cheddar.gui import settings
from cheddar.util.itertools import consecutive

IMG_SIZE = settings['table_view_img_height']


class TableViewTab(QtGui.QWidget):
    """GUI table view tab class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QtGui.QHBoxLayout(self)
        self.table = Table(self)
        layout.addWidget(self.table)
        self.setLayout(layout)


class Table(QtGui.QTableWidget):

    tableSelected = QtCore.Signal()

    def __init__(self, parent=None):
        self.parent = parent
        self.df = parent.parent.parent.df
        super().__init__(self.df.row_count(), len(self.df.header()), parent)

        self.vheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Vertical)
        self.vheader.setResizeMode(QtGui.QHeaderView.Fixed)
        self.vheader.setVisible(False)
        self.setVerticalHeader(self.vheader)
        self.hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        self.hheader.setResizeMode(QtGui.QHeaderView.Fixed)
        self.setHorizontalHeader(self.hheader)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.itemSelectionChanged.connect(self.update_selection)

    def update_all(self):
        self.df = self.parent.parent.parent.df
        self.clear()
        self.setColumnCount(len(self.df.header()))
        self.setRowCount(self.df.row_count())
        self.setHorizontalHeaderLabels(self.df.header())
        for j, col in enumerate(self.df.header()):
            for i in range(self.df.row_count()):
                if self.df[col].type == "qsvg":
                    self.setCellWidget(i, j, self.df[col][i].widget(self))
                else:
                    item = QtGui.QTableWidgetItem(str(self.df[col][i]))
                    self.setItem(i, j, item)
        self.flush_view()

    def init_view(self, row_count):
        self.df = self.parent.parent.parent.df
        self.clear()
        self.setColumnCount(len(self.df.header()))
        self.setRowCount(row_count)
        self.setHorizontalHeaderLabels(self.df.header())

    def add_rows(self, start, end):
        self.df = self.parent.parent.parent.df
        for j, col in enumerate(self.df.header()):
            for i in range(start, end):
                cell = self.df[col][i]
                if self.df[col].type == "qsvg":
                    self.setCellWidget(i, j, cell.widget(self))
                else:
                    item = QtGui.QTableWidgetItem(str(cell))
                    self.setItem(i, j, item)

    def flush_view(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    @QtCore.Slot()
    def update_selection(self):
        """Get selected cells in table view as tab-separeted values.
        (for copy and paste multiple cells)
        """
        model = self.model()
        idxs = sorted(self.selectionModel().selectedIndexes())
        contents = []
        for f, s in consecutive(idxs, 2):
            contents.append(str(model.data(f)))
            if f.row() == s.row():
                contents.append("\t")
            else:
                contents.append("\n")
        contents.append(str(model.data(idxs[-1])))
        self.parent.parent.parent.selection = "".join(contents)
        self.parent.parent.parent.copy_action.setEnabled(True)
