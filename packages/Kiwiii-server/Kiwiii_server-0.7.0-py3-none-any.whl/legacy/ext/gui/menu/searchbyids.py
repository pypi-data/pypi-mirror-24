
import yaml
from PySide import QtGui, QtCore

from cheddar.chem.draw.qtcanvas import QSvgCanvas
from cheddar.chem.draw.moldrawable import draw
from cheddar.chem.draw.qsvg import QSvg
from cheddar.chem.v2000supplier import ctab_to_compound
from cheddar.chem.model.graphmol import build
from cheddar.data.pandasdataframe import build as dfbuild
from cheddar.gui.helperwidget import ComboBoxWidget, PasteAreaWidget
from cheddar.gui.helperwidget import ButtonBoxWidget
from cheddar.gui.threading import Thread, WorkerObject

GROUP = "File"
NAME = "Search by IDs"

with open("./datasource/db_info.yaml") as file:
    DB_INFO = yaml.load(file.read())


class SearchByIdsAction(QtGui.QAction):

    def __init__(self, parent=None, name=NAME):
        super().__init__(name, parent, triggered=self.execute)
        self.parent = parent
        self.thread = None

    @QtCore.Slot()
    def execute(self):
        dialog = SearchByIdsDialog(self.parent)
        if dialog.exec_():
            self.thread = Thread(self.parent)
            worker = SearchByIdsWorker(self.parent, dialog.query)
            self.thread.launch_worker(worker)
            self.thread.worker.invoke_method("start")


class SearchByIdsWorker(WorkerObject):

    updated = QtCore.Signal()

    def __init__(self, mainwindow, query, db_info=DB_INFO):
        super().__init__()
        self.mainw = mainwindow
        self.db_info = db_info
        self.db = query["db"]
        self.ids = query["ids"]
        self.updated.connect(self.mainw.update_all)

    @QtCore.Slot()
    def start(self):
        from cheddar.data.sqliteconnection import CON
        CON.connect(
            "./datasource/{}".format(self.db_info[self.db]['path']),
            self.db_info[self.db]['table']
        )
        p_key = self.db_info[self.db]['primary_key']
        s_col = self.db_info[self.db]['structure_column']
        v_cols = self.db_info[self.db]['visible_columns']
        cols = ["#index", "#mol", "#svg", p_key] + v_cols
        types = ["int", "object", "qsvg", "str"]
        types.extend(["text"] * len(v_cols))
        self.mainw.df = dfbuild(names=cols, types=types)
        self.mainw.df["#mol"].visible = False
        canvas = QSvgCanvas()
        # Use findbykey to avoid automatic sort of primary keys.
        # This may be less efficient than using findbykeys (below)
        for i, id_ in enumerate(self.ids):
            res = next(CON.findbykey(p_key, id_))
            row = {col: res[j] for j, col in enumerate(CON.columns)}
            row['#index'] = str(i + 1)
            row['#mol'] = build(ctab_to_compound(row[s_col]))
            row['#svg'] = draw(row['#mol'], canvas, QSvg())
            self.mainw.df.append(row)
        """
        for i, res in enumerate(CON.findbykeys(p_key, self.ids)):
            row = {col: res[j] for j, col in enumerate(CON.columns)}
            row['#index'] = str(i + 1)
            row['#mol'] = build(ctab_to_compound(row[s_col]))
            row['#svg'] = draw(row['#mol'], canvas, QSvg())
            self.mainw.df.append(row)
        """
        self.updated.emit()
        self.finished.emit()


class SearchByIdsDialog(QtGui.QDialog):

    def __init__(self, parent=None, db_info=DB_INFO):
        super().__init__(parent)
        self.db_info = db_info
        self.setWindowTitle(NAME)
        self.query = {"db": "", "ids": []}

        self.cbox = ComboBoxWidget(
            self.db_info.keys(), "Select datasource:", self)
        self.textarea = PasteAreaWidget(
            "Copy and paste Compound IDs from Excel worksheet.", self)
        self.textarea.textEntered.connect(self.enable_submit)
        self.textarea.noTextEntered.connect(self.disable_submit)

        self.buttons = ButtonBoxWidget(self)
        self.buttons.ok.setDisabled(True)
        self.buttons.accepted.connect(self.ok)
        self.buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.cbox)
        layout.addWidget(self.textarea)
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        self.resize(500, 600)

    @QtCore.Slot()
    def enable_submit(self):
        self.buttons.ok.setEnabled(True)

    @QtCore.Slot()
    def disable_submit(self):
        self.buttons.ok.setDisabled(True)

    def ok(self):
        combo = self.cbox.selected()
        ids = self.textarea.lines()
        while "" in ids:
            ids.remove("")
        if len(ids):
            self.query = {"db": combo, "ids": ids}
            self.accept()
