
from PySide import QtGui, QtCore

from cheddar.data.csvsupplier import csv_supplier, scan, ParseOption
from cheddar.data.pandasdataframe import build
from cheddar.gui.helperwidget import ButtonBoxWidget, SelectFileWidget
from cheddar.gui.helperwidget import CheckBoxListWidget
from cheddar.gui.threading import Thread, WorkerObject

GROUP = "File"
NAME = "Import CSV"


class ImportCsvAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent
        self.thread = None

    @QtCore.Slot()
    def execute(self):
        dialog = ImportCsvDialog(self.parent)
        if dialog.exec_():
            self.thread = Thread(self.parent)
            worker = ImportCsvWorker(self.parent, dialog.query)
            self.thread.launch_worker(worker)
            self.thread.worker.invoke_method("start")


class ImportCsvWorker(WorkerObject):

    updated = QtCore.Signal()
    finished = QtCore.Signal()

    def __init__(self, mainwindow, query):
        super().__init__()
        self.mainw = mainwindow
        self.path = query["path"]
        self.selected = query["selected"]
        self.row_count = query["row_count"]
        self.updated.connect(self.mainw.update_all)

    @QtCore.Slot()
    def start(self):
        cols = self.selected
        types = ["text"] * len(cols)
        opt = ParseOption()
        if self.path.split(".")[1] == "txt":
            opt.delimiter = "\t"
        self.mainw.df = build(names=cols, types=types)
        for i, row in enumerate(csv_supplier(self.path, opt)):
            self.mainw.df.append(row)
        self.updated.emit()
        self.finished.emit()


class ImportCsvDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(NAME)
        self.query = {"path": "", "selected": [], "row_count": 0}

        self.file_widget = SelectFileWidget(
            "File path:", "Tab Separated Values (*.txt);;CSV (*.csv)", self)
        self.file_widget.textEntered.connect(self.enable_scan)
        self.file_widget.noTextEntered.connect(self.disable_scan)
        self.scan_button = QtGui.QPushButton("Scan", self)
        self.scan_button.clicked.connect(self.scan)

        self.list_widget = CheckBoxListWidget(
            None, "Select fields for import", self)
        self.list_widget.anyItemChecked.connect(self.enable_submit)
        self.list_widget.noItemChecked.connect(self.disable_submit)

        self.buttons = ButtonBoxWidget(self)
        self.buttons.ok.setDisabled(True)
        self.buttons.accepted.connect(self.ok)
        self.buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.file_widget)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        self.resize(500, 600)

    @QtCore.Slot()
    def enable_scan(self):
        self.query["path"] = self.file_widget.lineedit.text()
        self.scan_button.setEnabled(True)

    @QtCore.Slot()
    def disable_scan(self):
        self.scan_button.setDisabled(True)

    def scan(self):
        self.list_widget.list.clear()
        opt = ParseOption()
        if self.query["path"].split(".")[1] == "txt":
            opt.delimiter = "\t"
        cols, count = scan(self.query["path"], opt)
        self.query["row_count"] = count
        cols.sort()
        for col in cols:
            self.list_widget.add_item(col)

    @QtCore.Slot()
    def enable_submit(self):
        self.buttons.ok.setEnabled(True)

    @QtCore.Slot()
    def disable_submit(self):
        self.buttons.ok.setDisabled(True)

    @QtCore.Slot()
    def ok(self):
        self.query["selected"] = self.list_widget.selected()
        self.accept()
