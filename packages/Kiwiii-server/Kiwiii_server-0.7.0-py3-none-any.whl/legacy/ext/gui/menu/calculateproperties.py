
from PySide import QtGui, QtCore
from cheddar.gui.helperwidget import ButtonBoxWidget
from cheddar.gui.helperwidget import CheckBoxListWidget
from cheddar.gui.threading import Thread, WorkerObject

GROUP = "Edit"
NAME = "Calculate properties"


class CalculatePropertiesAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent
        self.thread = None

    @QtCore.Slot()
    def execute(self):
        dialog = CalculatePropertiesDialog(self.parent)
        if dialog.exec_():
            self.thread = Thread(self.parent)
            worker = CalculatePropertiesWorker(self.parent, dialog.query)
            self.thread.launch_worker(worker)
            self.thread.worker.invoke_method("start")


class CalculatePropertiesWorker(WorkerObject):

    updated = QtCore.Signal()

    def __init__(self, mainwindow, query):
        super().__init__()
        self.mainw = mainwindow
        self.selected = query["selected"]
        self.updated.connect(self.mainw.update_all)

    @QtCore.Slot()
    def start(self):
        funcs = {"MW": lambda x: x.mw()}
        for e in self.selected:
            self.mainw.df["#mol"].apply(e, funcs[e], type_="float")
        self.updated.emit()
        self.finished.emit()


class CalculatePropertiesDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(NAME)
        self.query = {"selected": []}

        self.list_widget = CheckBoxListWidget(
            ["MW"], "Select calculated columns", self)
        self.list_widget.anyItemChecked.connect(self.enable_submit)
        self.list_widget.noItemChecked.connect(self.disable_submit)

        self.buttons = ButtonBoxWidget(self)
        self.buttons.ok.setDisabled(True)
        self.buttons.accepted.connect(self.ok)
        self.buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        self.resize(500, 600)

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
