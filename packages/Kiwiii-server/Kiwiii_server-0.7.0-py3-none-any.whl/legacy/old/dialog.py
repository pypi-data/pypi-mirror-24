# coding: UTF-8

"""
GUI dialog module
"""

import sys

from PySide import QtGui, QtCore

from tmp import settings


class ImportDb(QtGui.QDialog):
    """Dialog to select database and input ID list

    Attribute:
      query: (input ID list, sqlite table name)
    """

    def __init__(self, parent=None):
        super(ImportDb, self).__init__(parent)

        self.query = []
        self._table_list = settings.DB_TABLE_MAPPING["data"]
        self._db_buttons = []
        for dict_ in self._table_list:
            self._db_buttons.append(QtGui.QRadioButton(dict_["name"], self))
        self._db_buttons[0].setChecked(True)
        self._textarea = QtGui.QTextEdit(self)
        label1 = QtGui.QLabel("Database")
        label2 = QtGui.QLabel(
            "Copy and paste compound ID list from Excel worksheet.")
        button = QtGui.QPushButton("Submit", self)
        button.clicked.connect(self.button_clicked)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label1)
        for obj in self._db_buttons:
            layout.addWidget(obj)
        layout.addWidget(label2)
        layout.addWidget(self._textarea)
        layout.addWidget(button)
        self.setLayout(layout)

        self.setWindowTitle("Import compound List")
        self.resize(500, 600)

    def button_clicked(self):
        db = ""
        for i, obj in enumerate(self._db_buttons):
            if obj.isChecked():
                db = self._table_list[i]["table"]
        id_text = self._textarea.toPlainText()
        ids = id_text.split("\n")
        while "" in ids:
            ids.remove("")
        self.query = (ids, db)
        self.accept()


class AddDrc(QtGui.QDialog):
    """Dialog to select logical assay file from Genedata Database

    Attribute:
      reportkey: logicalAssayReportKey
      reportname: logicalAssayReportName
      options: cheddar.java.DRCOptions
    """
    def __init__(self, logical_assay_list, parent=None):
        super(AddDrc, self).__init__(parent)
        self.reportkey = None
        self.reportname = None
        from tmp.java import DRCOptions
        self.options = DRCOptions()
        self._reportlist = logical_assay_list

        """AC50 unit"""
        unit_box = QtGui.QWidget()
        unit_layout = QtGui.QHBoxLayout()
        unit_label = QtGui.QLabel("AC50 unit")
        self._unit_combo = QtGui.QComboBox()
        self._unit_combo.addItems(["uM", "nM", "log"])
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self._unit_combo)
        unit_layout.addStretch(1)
        unit_layout.setContentsMargins(0, 0, 0, 0)
        unit_box.setLayout(unit_layout)
        """Activity range"""
        range_box = QtGui.QWidget()
        range_layout = QtGui.QHBoxLayout()
        self._range_check = QtGui.QCheckBox("Set activity range", self)
        self._range_check.setChecked(True)
        self._range_check.stateChanged.connect(self.range_check_statechanged)
        self._range_min_spin = QtGui.QSpinBox(self)
        self._range_min_spin.setRange(-1000, 1000)
        self._range_min_spin.setValue(-20)
        self._range_min_spin.valueChanged.connect(self.range_min_spin_valuechanged)
        range_mid_label = QtGui.QLabel("-")
        self._range_max_spin = QtGui.QSpinBox(self)
        self._range_max_spin.setRange(-1000, 1000)
        self._range_max_spin.setValue(120)
        self._range_max_spin.valueChanged.connect(self.range_max_spin_valuechanged)
        range_range_label = QtGui.QLabel("(-1000 - 1000)")
        range_layout.addWidget(self._range_check)
        range_layout.addWidget(self._range_min_spin)
        range_layout.addWidget(range_mid_label)
        range_layout.addWidget(self._range_max_spin)
        range_layout.addWidget(range_range_label)
        range_layout.addStretch(1)
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_box.setLayout(range_layout)
        """AC50, nHill digits"""
        digit_box = QtGui.QWidget()
        digit_layout = QtGui.QHBoxLayout()
        ac50_label = QtGui.QLabel("AC50 digits")
        self._ac50_spin = QtGui.QSpinBox(self)
        self._ac50_spin.setValue(5)
        self._ac50_spin.setRange(0, 8)
        ac50_range_label = QtGui.QLabel("(0 - 8)")
        hill_label = QtGui.QLabel("nHill digits")
        self._hill_spin = QtGui.QSpinBox(self)
        self._hill_spin.setValue(3)
        self._hill_spin.setRange(0, 8)
        hill_range_label = QtGui.QLabel("(0 - 8)")
        digit_layout.addWidget(ac50_label)
        digit_layout.addWidget(self._ac50_spin)
        digit_layout.addWidget(ac50_range_label)
        digit_layout.addStretch(1)
        digit_layout.addWidget(hill_label)
        digit_layout.addWidget(self._hill_spin)
        digit_layout.addWidget(hill_range_label)
        digit_layout.addStretch(1)
        digit_layout.setContentsMargins(0, 0, 0, 0)
        digit_box.setLayout(digit_layout)
        """DRCOptions group"""
        options_group = QtGui.QGroupBox("DRC options")
        options_layout = QtGui.QVBoxLayout()
        options_layout.addWidget(unit_box)
        options_layout.addWidget(range_box)
        options_layout.addWidget(digit_box)
        options_group.setLayout(options_layout)

        """Folder tree"""
        label_selectfile = QtGui.QLabel("Select logical assay file")
        tree = QtGui.QTreeWidget()
        tree.setMinimumHeight(300)
        treeitem = QtGui.QTreeWidgetItem(tree)
        treeitem.setText(0, "Genedata screener database")
        tree.setItemExpanded(treeitem, True)
        # reportlist = self.testdict
        for k, v in self._reportlist.items():
            itemdir = v[0].split("/")
            itemdir.pop(0)
            parent = treeitem
            child = None
            ### Search folder
            for i in itemdir:
                is_dir_exist = False
                # print "cycle: " + i
                # print "parent: " + parent.text(0)
                # print "Num of child: " + str(parent.childCount())
                ### If the folder exist, search child folder
                for j in range(parent.childCount()):
                    if parent.child(j).text(0) == i:
                        parent = parent.child(j)
                        is_dir_exist = True
                        # print "exist dir: " + i + "\n"
                        break
                ### If the folder doesn't exist, add new folder
                if not is_dir_exist:
                    child = QtGui.QTreeWidgetItem(parent)
                    child.setText(0, i)
                    # print "new dir: " + i + "\n"
                    parent = child
            ### Add widget to the node
            item = QtGui.QTreeWidgetItem()
            item.setText(0, k)
            item.setText(1, v[0])
            parent.addChild(item)
            parent.sortChildren(0, QtCore.Qt.AscendingOrder)
            # print "add file: " + v[0] + "\n"
        tree.itemDoubleClicked.connect(self.item_doubleclicked)
        """Dialog layout"""
        layout = QtGui.QVBoxLayout()
        layout.addWidget(options_group)
        layout.addWidget(label_selectfile)
        layout.addWidget(tree)
        self.setLayout(layout)
        self.setWindowTitle("Add dose-response curve")
        self.setMinimumWidth(500)
        self.adjustSize()

    def item_doubleclicked(self, item):
        """
        Args:
          item: doubleclicked item in TreeWidget
        """
        if item.childCount() == 0:
            for k, v in self._reportlist.items():
                if k == item.text(0) and v[0] == item.text(1):
                    self.reportkey = v[1]
                    self.reportname = k
        if self._range_check.isChecked():
            self.options.activity_range = (
                self._range_min_spin.value(), self._range_max_spin.value()
            )
        self.options.ac50_unit_type = self._unit_combo.currentText()
        self.options.ac50_digits = self._ac50_spin.value()
        self.options.hill_digits = self._hill_spin.value()
        self.accept()

    def range_check_statechanged(self):
        """Toggle spinbox state if the checkbox was checked"""
        if self._range_check.isChecked():
            self._range_min_spin.setDisabled(False)
            self._range_max_spin.setDisabled(False)
            self._range_min_spin.setStyleSheet("QSpinBox { color: #000000; }")
            self._range_max_spin.setStyleSheet("QSpinBox { color: #000000; }")
        else:
            self._range_min_spin.setDisabled(True)
            self._range_max_spin.setDisabled(True)
            self._range_min_spin.setStyleSheet("QSpinBox { color: #999999; }")
            self._range_max_spin.setStyleSheet("QSpinBox { color: #999999; }")

    def range_min_spin_valuechanged(self):
        """min value must be always smaller than max value"""
        if self._range_min_spin.value() > self._range_max_spin.value():
            self._range_max_spin.setValue(self._range_min_spin.value())

    def range_max_spin_valuechanged(self):
        """max value must be always larger than min value"""
        if self._range_max_spin.value() < self._range_min_spin.value():
            self._range_min_spin.setValue(self._range_max_spin.value())


class Wait(QtGui.QDialog):
    """Wait dialog"""
    def __init__(self, parent=None):
        super(Wait, self).__init__(parent)
        label1 = QtGui.QLabel("Please wait...")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label1)
        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Work in progress")
        self.resize(200, 100)
        self.setModal(True)
        self.show()
        self.raise_()
        QtGui.QApplication.processEvents()


class OpenFile(QtGui.QFileDialog):
    """Dialog to choose file

    Attribute:
      path: file to be opened
    """
    def __init__(self, parent=None):
        super(OpenFile, self).__init__(parent)
        self.path = None
        self.setFileMode(QtGui.QFileDialog.ExistingFile)
        filename, _ = self.getOpenFileName(
            self, "Open", "~/", "SDFile (*.sdf)")
        if filename:
            self.path = filename
            self.accept()


class SaveFile(QtGui.QFileDialog):
    """Dialog to enter file name to be saved

    Attribute:
      path: file to be saved
    """
    def __init__(self, parent=None):
        super(SaveFile, self).__init__(parent)
        self.path = None
        self.setFileMode(QtGui.QFileDialog.AnyFile)
        filename, _ = self.getSaveFileName(
            self, "Save As", "~/", "Excel worksheet (*.xlsx)")
        if filename:
            self.path = filename
            self.accept()


def main():
    QtGui.QApplication(sys.argv)
    widget = AddDrc()
    widget.exec_()
    sys.exit()

if __name__ == "__main__":
    main()
