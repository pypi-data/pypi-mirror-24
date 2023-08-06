
import sys

from PySide import QtGui

from cheddar.gui import mainwindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = mainwindow.MainWindow()
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())
