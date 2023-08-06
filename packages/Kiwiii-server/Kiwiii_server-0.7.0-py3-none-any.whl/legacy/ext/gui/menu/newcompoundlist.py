
from PySide import QtGui, QtCore

from cheddar.data.pandasdataframe import build

GROUP = "File"
NAME = "New Compound List"


class NewCompoundListAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(NAME, parent, triggered=self.execute)
        self.parent = parent

    def execute(self):
        dialog = NewCompoundListDialog(self.parent)
        if dialog.exec_():
            self.parent.tab.start_loading()
            thread = NewCompoundListExec(self)
            thread.ids = dialog.query
            thread.finished.connect(self.parent.tab.finish_loading)
            thread.start()


class NewCompoundListExec(QtCore.QThread):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ids = None

    def run(self):
        self.parent.parent.df = build(data={"ID": self.ids})


class NewCompoundListDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(NAME)

        self.query = []
        top_label = QtGui.QLabel(
            "Copy and paste compound ID list from Excel worksheet.", self)
        self.textarea = QtGui.QTextEdit(self)
        self.textarea.textChanged.connect(self.text_changed)
        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal,
            self)
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.reject)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(top_label)
        layout.addWidget(self.textarea)
        layout.addWidget(self.button_box)
        self.setLayout(layout)
        self.resize(500, 600)

    def text_changed(self):
        if self.textarea.toPlainText():
            self.button_box.button(
                QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.button_box.button(
                QtGui.QDialogButtonBox.Ok).setDisabled(True)

    def ok(self):
        id_text = self.textarea.toPlainText()
        ids = id_text.split("\n")
        while "" in ids:
            ids.remove("")
        if len(ids):
            self.query = ids
            self.accept()
        else:
            self.submit_box.set_error_label("Enter compound list")
