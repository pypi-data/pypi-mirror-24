
import glob
import os

from PySide import QtGui, QtCore

GROUP = "Open"
NAME = "Search Database"


class SearchDatabaseAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent

    def execute(self):
        dialog = SearchDatabaseDialog(self.parent)
        if dialog.exec_():
            self.parent.tab.start_loading()
            thread = SearchDatabaseExec(dialog.db, dialog.query, self)
            thread.finished.connect(self.parent.tab.finish_loading)
            thread.start()


class SearchDatabaseExec(QtCore.QThread):

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        from cheddar.data.sqliteconnection import CON
        CON.connect("./datasource/{}.sqlite3".format(self.db))
        df = build_from_rows(CON.column_list())
        for row in CON.select_rows_iter("DRUGBANK_ID", self.ids):
            df.append(row)
        self.parent.parent.df = df


class SearchDatabaseDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(NAME)
        self.db = None
        self.column = None
        self.query = []

        cbox_widget = QtGui.QWidget(self)
        cbox_label = QtGui.QLabel("Select datasource", cbox_widget)
        self.cbox = QtGui.QComboBox(cbox_widget)
        for sq in glob.glob("./datasource/*.sqlite3"):
            self.cbox.addItem(os.path.basename(sq).split(".")[0])
        cbox_layout = QtGui.QHBoxLayout(cbox_widget)
        cbox_layout.addWidget(cbox_label)
        cbox_layout.addWidget(self.cbox)
        cbox_widget.setLayout(cbox_layout)

        col_widget = QtGui.QWidget(self)
        col_label = QtGui.QLabel("Column:", col_widget)
        col_combo = QtGui.QComboBox(col_widget)
        col_combo.setDisabled(True)
        col_combo.currentIndexChanged.connect(self.col_changed)
        col_layout = QtGui.QHBoxLayout(col_widget)
        col_layout.addWidget(col_label)
        col_layout.addWidget(col_combo)
        col_widget.setLayout(col_layout)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(db_widget)
        layout.addWidget(col_widget)
        self.setLayout(layout)

    def db_changed(self):
        self.db = self.db_combo.currentIndex()

    def text_changed(self):
        if self.textarea.toPlainText():
            self.button_box.button(
                QtGui.QDialogButtonBox.Ok).setEnabled(True)
            return
        self.button_box.button(
            QtGui.QDialogButtonBox.Ok).setDisabled(True)