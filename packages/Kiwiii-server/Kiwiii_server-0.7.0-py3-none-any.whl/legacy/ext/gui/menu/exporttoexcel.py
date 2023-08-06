
from PySide import QtGui, QtCore

from cheddar.data.excelexporter import export

GROUP = "File"
NAME = "Export to Excel"

ACTION_CLASS = "ExportToExcelAction"


class ExportToExcelAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent

    def execute(self):
        path, _ = QtGui.QFileDialog.getSaveFileName(
            self.parent, "Save as", "~/", "Excel spreadsheet (*.xlsx)")
        if path:
            self.parent.tab.start_loading()
            thread = ExportToExcelExec(path, self)
            thread.finished.connect(self.parent.tab.finish_loading)
            thread.start()


class ExportToExcelExec(QtCore.QThread):

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.path = path

    def run(self):
        export(self.parent.parent.df, self.path)
