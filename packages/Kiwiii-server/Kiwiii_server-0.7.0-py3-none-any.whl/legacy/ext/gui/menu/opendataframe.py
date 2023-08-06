
from PySide import QtGui, QtCore

from cheddar.data.sqliteconnection import resume_df

GROUP = "File"
NAME = "Open Dataframe"


class OpenDataframeAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent
        self.thread = QtCore.QThread()
        self.worker = None

    def execute(self):
        path, _ = QtGui.QFileDialog.getOpenFileName(
            self.parent, "Open", "~/", "Cheddar dataframe (*.chd)")
        if path:
            self.parent.tab.start_loading()
            self.worker = OpenDataframeWorker(self.parent, path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.finish)
            self.thread.start()

    def finish(self):
        self.parent.update_all()
        self.thread.quit()


class OpenDataframeWorker(QtCore.QThread):

    finished = QtCore.Signal()

    def __init__(self, mainwindow, path):
        super().__init__()
        self.mainw = mainwindow
        self.path = path

    def run(self):
        self.mainw.df = resume_df(self.path)
        self.finished.emit()