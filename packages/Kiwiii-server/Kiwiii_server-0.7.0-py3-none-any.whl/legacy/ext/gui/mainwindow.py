
import math
from PySide import QtCore, QtGui

from cheddar.data.pandasdataframe import build
from cheddar.gui.menu.calculateproperties import CalculatePropertiesAction
from cheddar.gui.menu.copy import CopyAction
from cheddar.gui.menu.exporttoexcel import ExportToExcelAction
from cheddar.gui.menu.importcsv import ImportCsvAction
from cheddar.gui.menu.importsdfile import ImportSdfileAction
from cheddar.gui.menu.newcompoundlist import NewCompoundListAction
from cheddar.gui.menu.opendataframe import OpenDataframeAction
from cheddar.gui.menu.savedataframe import SaveDataframeAction
from cheddar.gui.menu.searchbyids import SearchByIdsAction
from cheddar.gui.menu.searchbyidsdemo import SearchByIdsActionDemo
from cheddar.gui.structureviewtab import StructureViewTab
from cheddar.gui.tableviewtab import TableViewTab


class MainWindow(QtGui.QMainWindow):
    """GUI main window class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.threads = []

        filemenu = self.menuBar().addMenu("File")
        filemenu.addAction(OpenDataframeAction(self))
        filemenu.addAction(SaveDataframeAction(self))
        filemenu.addSeparator()
        filemenu.addAction(SearchByIdsAction(self))
        filemenu.addAction(ImportSdfileAction(self))
        self.import_csv_action = ImportCsvAction(self)
        filemenu.addAction(self.import_csv_action)
        filemenu.addSeparator()
        filemenu.addAction(ExportToExcelAction(self))

        editmenu = self.menuBar().addMenu("Edit")
        editmenu.addAction(CalculatePropertiesAction(self))
        self.copy_action = CopyAction(self)
        editmenu.addAction(self.copy_action)

        plgmenu = self.menuBar().addMenu("Plugin")

        devmenu = self.menuBar().addMenu("Developer")
        devmenu.addAction(SearchByIdsActionDemo(self))
        devmenu.addAction(NewCompoundListAction(self))

        """ Dynamic import
        from os.path import basename, splitext
        import glob
        import importlib
        action_dir = "cheddar/extentions/gui/menu"
        action_mods = glob.glob("{}/*".format(action_dir))
        for path in action_mods:
            mod_name = ".".join(
                [action_dir.replace("/", "."), splitext(basename(path))[0]])
            try:
                mod = importlib.import_module(mod_name)
                action = getattr(mod, getattr(mod, "ACTION_CLASS"))
                group = getattr(mod, "GROUP")
            except (AttributeError, ImportError):
                pass
        """

        self.selection = None
        self.df = build()

        self.tab = MainTab(self)
        self.setCentralWidget(self.tab)
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle("Compound search")
        self.resize(1000, 800)

        self.total_chunks = 0
        self.processed_chunks = 0

    @QtCore.Slot()
    def update_all(self):
        self.tab.struct_view.view.update_all()
        self.tab.table_view.table.update_all()
        self.status_bar.finish_process()

    @QtCore.Slot()
    def init_view(self, row_count, chunks):
        self.total_chunks = chunks
        self.processed_chunks = 0
        self.tab.struct_view.view.init_view()
        self.tab.table_view.table.init_view(row_count)

    @QtCore.Slot()
    def add_rows(self, start, end):
        # print("start: {}".format(end))
        self.tab.struct_view.view.add_rows(start, end)
        self.tab.table_view.table.add_rows(start, end)
        self.processed_chunks += 1
        self.status_bar.progress(
            math.ceil(self.processed_chunks / self.total_chunks * 100))
        if self.processed_chunks == self.total_chunks:
            self.flush_view()

    @QtCore.Slot()
    def insert_column(self, col, pos):
        pass

    def flush_view(self):
        # print("Loading finished")
        self.tab.struct_view.view.flush_view()
        self.tab.table_view.table.flush_view()
        self.status_bar.finish_process()

    """
    def eventFilter(self, obj, event):
        if self.user_input_lock:
            print("invalid input: {}".format(event.type()))
            return True
        else:
            return QtGui.QMainWindow.eventFilter(self, obj, event)
    """

    def closeEvent(self, event):
        print("attempt to close")
        if self.threads:
            for t in self.threads:
                if t.isRunning():
                    t.abort()
                    print("QThread aborted")
        print("closed")
        event.accept()


class StatusBar(QtGui.QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_bar = QtGui.QProgressBar(self)
        self.progress_bar.setMaximumWidth(280)
        self.circle = QtGui.QLabel(self)
        movie = QtGui.QMovie("./lib/loading.gif")
        movie.setScaledSize(QtCore.QSize(16, 16))
        self.circle.setMovie(movie)
        movie.start()
        self.progress_bar.setVisible(False)
        self.circle.setVisible(False)
        self.addPermanentWidget(self.circle)
        self.addPermanentWidget(self.progress_bar)
        self.showMessage("Ready")

    def start_process(self):
        self.progress_bar.setVisible(True)
        self.circle.setVisible(True)
        self.showMessage("Now loading...")

    def progress(self, value):
        self.progress_bar.setValue(value)

    def finish_process(self):
        self.progress_bar.setVisible(False)
        self.circle.setVisible(False)
        self.showMessage("Loading finished")


class MainTab(QtGui.QTabWidget):
    """GUI main tab class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.df = None
        self.struct_view = StructureViewTab(self)
        self.table_view = TableViewTab(self)
        self.addTab(self.struct_view, "Structure view")
        self.addTab(self.table_view, "Table view")
