
from PySide import QtGui, QtCore

from cheddar.data.sqliteconnection import save_df

GROUP = "File"
NAME = "Save Dataframe"


class SaveDataframeAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent
        self.thread = QtCore.QThread()
        self.worker = None

    def execute(self):
        path, _ = QtGui.QFileDialog.getSaveFileName(
            self.parent, "Save as", "~/", "Cheddar dataframe (*.chd)")
        if path:
            self.parent.tab.start_loading()
            self.worker = SaveDataframeWorker(self.parent, path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.finish)
            self.thread.start()

    def finish(self):
        self.parent.update_all()
        self.thread.quit()


class SaveDataframeWorker(QtCore.QObject):

    def __init__(self, mainwindow, path):
        super().__init__()
        self.mainw = mainwindow
        self.path = path

    def run(self):
        save_df(self.mainw.df, self.path)
        self.finished.emit()
