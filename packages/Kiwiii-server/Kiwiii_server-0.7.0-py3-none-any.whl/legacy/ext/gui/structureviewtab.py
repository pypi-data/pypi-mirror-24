
import math

from PySide import QtCore, QtGui


class StructureViewTab(QtGui.QWidget):
    """GUI structure view tab class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QtGui.QVBoxLayout(self)
        self.view = StructureView(self)
        layout.addWidget(self.view)
        self.setLayout(layout)


class StructureView(QtGui.QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.df = parent.parent.parent.df
        self.widget = QtGui.QWidget(self)
        self.setWidget(self.widget)
        self.layout = None

    def update_all(self):
        self.df = self.parent.parent.parent.df
        if '#svg' not in self.df.header(visible_only=False):
            return
        self.widget = QtGui.QWidget(self)
        self.layout = QtGui.QGridLayout(self.widget)
        for i, row in self.df.rows_iter():
            molpanel = QtGui.QWidget(self.widget)
            mol_layout = QtGui.QVBoxLayout(molpanel)
            mol_layout.addWidget(row['#svg'].widget())
            mol_layout.addWidget(QtGui.QLabel(row['#index']))
            molpanel.setLayout(mol_layout)
            p_row = math.floor(i / 4)
            p_col = i % 4
            self.layout.addWidget(molpanel, p_row, p_col)
        self.flush_view()

    def init_view(self):
        self.df = self.parent.parent.parent.df
        if '#svg' not in self.df.header(visible_only=False):
            return
        self.widget = QtGui.QWidget(self)
        self.layout = QtGui.QGridLayout(self.widget)

    def add_rows(self, start, end):
        self.df = self.parent.parent.parent.df
        if '#svg' not in self.df.header(visible_only=False):
            return
        for i in range(start, end):
            molpanel = QtGui.QWidget(self.widget)
            mol_layout = QtGui.QVBoxLayout(molpanel)
            mol_layout.addWidget(self.df['#svg'][i].widget())
            mol_layout.addWidget(QtGui.QLabel(self.df['#index'][i]))
            molpanel.setLayout(mol_layout)
            p_row = math.floor(i / 4)
            p_col = i % 4
            self.layout.addWidget(molpanel, p_row, p_col)

    def flush_view(self):
        if '#svg' not in self.df.header(visible_only=False):
            return
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)