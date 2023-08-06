# coding: UTF-8

import sys

from PySide import QtGui

from tmp.cairotest import getPngImage


class MainWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        """ Main window components """
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(getPngImage(), "png")
        label = QtGui.QLabel()
        label.setPixmap(pixmap)
        label2 = QtGui.QLabel("hogehoge")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        self.setLayout(layout)

        self.setWindowTitle("Test")
        self.resize(500, 500)


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
