import yaml

from PySide import QtCore

from cheddar.gui.threading import Thread
from cheddar.gui.menu.searchbyids import SearchByIdsAction
from cheddar.gui.menu.searchbyids import SearchByIdsDialog
from cheddar.gui.menu.searchbyids import SearchByIdsWorker

GROUP = "Developer"
NAME = "Search by IDs(Demo)"

with open("./datasource/demo.yaml") as file:
    DB_INFO = yaml.load(file.read())


class SearchByIdsActionDemo(SearchByIdsAction):

    def __init__(self, parent=None):
        super().__init__(parent, NAME)

    @QtCore.Slot()
    def execute(self):
        dialog = SearchByIdsDialogDemo(self.parent)
        if dialog.exec_():
            self.thread = Thread(self.parent)
            worker = SearchByIdsWorkerDemo(self.parent, dialog.query)
            self.thread.launch_worker(worker)
            self.thread.worker.invoke_method("start")


class SearchByIdsWorkerDemo(SearchByIdsWorker):

    def __init__(self, mainwindow, query):
        super().__init__(mainwindow, query, DB_INFO)


class SearchByIdsDialogDemo(SearchByIdsDialog):

    def __init__(self, parent=None):
        super().__init__(parent, DB_INFO)
        self.textarea.textarea.setText("DB00928\nDB00929\nDB00930\nDB00931")