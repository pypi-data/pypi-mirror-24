import sys
from PySide import QtGui, QtCore


def main():
    #img = QtGui.QImage(QtCore.QSize(400, 400),
    #                   QtGui.QImage.Format_ARGB32_Premultiplied)
    pixmap = QtGui.QPixmap(QtCore.QSize(240, 240))
    font = QtGui.QFont("Helvetica", 40)

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
    painter.fillRect(0, 0, 240, 240, QtCore.Qt.white)
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine)
    painter.setPen(pen)
    painter.setBrush(QtGui.QColor(0, 0, 0))

    path1 = QtGui.QPainterPath()
    path1.moveTo(0, 0)
    path1.lineTo(25, 60)
    painter.drawPath(path1)

    qtext = QtGui.QTextDocument()
    qtext.setDefaultFont(font)
    qtext.setHtml("<span style='color:red;'>hoge<sub>hoge</sub></red>")
    p1 = QtCore.QPointF(120, 120)
    painter.translate(p1)
    qtext.drawContents(painter)
    painter.end()
    pixmap.save("hoge.png")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main()

"""
path
import pyqtgraph as pg
from pyqtgraph.graphicsItems.ArrowItem import ArrowItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph.exporters.ImageExporter import ImageExporter
app = QtGui.QApplication(sys.argv)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

w = pg.PlotWidget()

w.plotItem.hideAxis('left')
w.plotItem.hideAxis('bottom')

txt = TextItem('hoge')
alw = ArrowItem(angle=-20, tipAngle=30, baseAngle=-30, headLen=40, tailLen=None)
w.addItem(alw)
w.addItem(txt)
exporter = ImageExporter(alw)
exporter.export('hoge.png')
"""