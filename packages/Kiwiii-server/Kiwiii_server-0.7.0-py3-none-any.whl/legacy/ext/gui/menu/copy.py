
from PySide import QtGui

GROUP = "Edit"
NAME = "Copy"
DEPENDS = "TableViewTab"


class CopyAction(QtGui.QAction):

    def __init__(self, parent=None):
        super().__init__(
            NAME, parent, triggered=self.execute,
            shortcut=QtGui.QKeySequence.Copy
        )
        self.parent = parent
        self.setEnabled(False)

    def execute(self):
        data = self.parent.selection
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(data)

