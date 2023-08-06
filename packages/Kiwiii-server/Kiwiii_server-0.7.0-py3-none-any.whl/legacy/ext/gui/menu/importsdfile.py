
from PySide import QtGui, QtCore

from cheddar.chem.draw.qtcanvas import QSvgCanvas
from cheddar.chem.draw.qsvg import QSvg
from cheddar.chem.draw.moldrawable import draw
from cheddar.chem.model.graphmol import build
from cheddar.chem.v2000supplier import scan, compound_supplier
from cheddar.data.pandasdataframe import build as dfbuild
from cheddar.gui.threading import Thread, WorkerObject
from cheddar.gui.helperwidget import ButtonBoxWidget, SelectFileWidget
from cheddar.gui.helperwidget import CheckBoxListWidget

GROUP = "File"
NAME = "Import SDFile"


class ImportSdfileAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent
        self.thread = None

    @QtCore.Slot()
    def execute(self):
        dialog = ImportSdfileDialog(self.parent)
        if dialog.exec_():
            self.thread = Thread(self.parent)
            worker = ImportSdfileWorker(self.parent, dialog.query)
            self.thread.launch_worker(worker)
            self.thread.worker.invoke_method("start")


class ImportSdfileWorker(WorkerObject):

    initialized = QtCore.Signal(int, int)
    rowsAdded = QtCore.Signal(int, int)

    def __init__(self, mainwindow, query):
        super().__init__()
        self.mainw = mainwindow
        self.path = query["path"]
        self.selected = query["selected"]
        self.row_count = query["row_count"]
        self.initialized.connect(self.mainw.init_view)
        self.rowsAdded.connect(self.mainw.add_rows)

        self.supplier = None
        self.chunk_size = 100
        self.stopped = False
        self.count = 0
        self.canvas = QSvgCanvas()

    @QtCore.Slot()
    def start(self):
        cols = ["#index", "#mol", "#svg"] + self.selected
        coltype = ["int", "object", "qsvg"]
        coltype.extend(["text"] * len(self.selected))
        self.mainw.df = dfbuild(data=None, names=cols, types=coltype)
        self.mainw.df["#mol"].visible = False
        chunks = int(self.row_count / self.chunk_size) + 1
        self.supplier = compound_supplier(self.path)
        self.count = 0
        self.initialized.emit(self.row_count, chunks)
        self.invoke_method("process")

    @QtCore.Slot()
    def process(self):
        start = self.count
        for i in range(self.chunk_size):
            try:
                mol = next(self.supplier)
            except StopIteration:
                self.stopped = True
                break
            self.count += 1
            r = {'#index': str(self.count), '#mol': build(mol)}
            r['#svg'] = draw(r['#mol'], self.canvas, QSvg())
            for col in self.selected:
                r[col] = str(mol.options.get(col, ""))
            self.mainw.df.append(r)
        # print("emitted: {}".format(self.count))
        self.rowsAdded.emit(start, self.count)
        if self.stopped:
            self.finished.emit()
        else:
            self.invoke_method("process")

    @QtCore.Slot()
    def abort(self):
        self.stopped = True


class ImportSdfileDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(NAME)
        self.query = {"path": "", "selected": [], "row_count": 0}

        self.file_widget = SelectFileWidget(
            "SDFile path:", "SDFile (*.sdf)", self)
        self.file_widget.textEntered.connect(self.enable_scan)
        self.file_widget.noTextEntered.connect(self.disable_scan)
        self.scan_button = QtGui.QPushButton("Scan", self)
        self.scan_button.setDisabled(True)
        self.scan_button.clicked.connect(self.scan)

        self.list_widget = CheckBoxListWidget(
            None, "Select columns for import", self)
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

    @QtCore.Slot()
    def scan(self):
        self.list_widget.list.clear()
        cols, count = scan(self.query["path"])
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
