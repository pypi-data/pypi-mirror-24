
from PySide import QtCore, QtGui


class ComboBoxWidget(QtGui.QWidget):

    def __init__(self, items, label="Select:", parent=None):
        super().__init__(parent)

        self.label = QtGui.QLabel(label, self)
        self.cbox = QtGui.QComboBox(self)
        for e in items:
            self.cbox.addItem(e)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.cbox)
        self.setLayout(layout)

    def selected(self):
        return self.cbox.currentText()


class CheckBoxListWidget(QtGui.QWidget):

    anyItemChecked = QtCore.Signal()
    noItemChecked = QtCore.Signal()

    def __init__(self, items=None, label="Checklist:", parent=None):
        super().__init__(parent)
        self.label = QtGui.QLabel(label, self)
        self.list = QtGui.QListWidget(self)
        self.list.itemClicked.connect(self.is_any_checked)
        if items:
            for e in items:
                self.add_item(e)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def add_item(self, e):
        item = QtGui.QListWidgetItem(e, self.list)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)

    @QtCore.Slot()
    def is_any_checked(self):
        for i in range(self.list.count()):
            if self.list.item(i).checkState() is QtCore.Qt.Checked:
                self.anyItemChecked.emit()
                return
        self.noItemChecked.emit()

    def selected(self):
        result = []
        for i in range(self.list.count()):
            if self.list.item(i).checkState() is QtCore.Qt.Checked:
                result.append(self.list.item(i).text())
        return result


class PasteAreaWidget(QtGui.QWidget):

    textEntered = QtCore.Signal()
    noTextEntered = QtCore.Signal()

    def __init__(self, label="Textarea:", parent=None):
        super().__init__(parent)

        self.label = QtGui.QLabel(label, self)
        self.textarea = QtGui.QTextEdit(self)
        self.textarea.textChanged.connect(self.is_text_entered)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.textarea)
        self.setLayout(layout)

    def lines(self):
        return self.textarea.toPlainText().split("\n")

    @QtCore.Slot()
    def is_text_entered(self):
        if self.textarea.toPlainText():
            self.textEntered.emit()
        else:
            self.noTextEntered.emit()


class ButtonBoxWidget(QtGui.QWidget):

    accepted = QtCore.Signal()
    rejected = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cancel = QtGui.QPushButton("Cancel", self)
        self.cancel.clicked.connect(self.reject)
        self.ok = QtGui.QPushButton("OK", self)
        self.ok.clicked.connect(self.accept)
        layout = QtGui.QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.cancel)
        layout.addWidget(self.ok)
        self.setLayout(layout)

    @QtCore.Slot()
    def accept(self):
        self.accepted.emit()

    @QtCore.Slot()
    def reject(self):
        self.rejected.emit()


class SelectFileWidget(QtGui.QWidget):
    textEntered = QtCore.Signal()
    noTextEntered = QtCore.Signal()

    def __init__(self, label, filter_, parent=None):
        super().__init__(parent)

        self.filter = filter_
        self.label = QtGui.QLabel(label, self)
        self.lineedit = QtGui.QLineEdit(self)
        self.lineedit.textChanged.connect(self.is_text_entered)
        self.button = QtGui.QPushButton("...", self)
        self.button.clicked.connect(self.button_clicked)

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.lineedit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    @QtCore.Slot()
    def button_clicked(self):
        path, _ = QtGui.QFileDialog.getOpenFileName(
            self, "Open", "~/", self.filter)
        if path:
            self.lineedit.setText(path)

    @QtCore.Slot()
    def is_text_entered(self):
        if self.lineedit.text():
            self.textEntered.emit()
        else:
            self.noTextEntered.emit()