# coding: UTF-8

import math
import sys
import traceback

from PySide import QtGui, QtCore

import exception
from tmp import controller, datatable, dialog


class MainWindow(QtGui.QMainWindow):
    """GUI main window class"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self._table = datatable.Table()
        self._ctrl = controller.Controller(self._table)
        self._maintab = MainTab()
        self._create_actions()
        self._create_menus()
        self.setCentralWidget(self._maintab)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle("Compound search")
        self.resize(1000, 800)

    def _create_actions(self):
        self._import_db_action = QtGui.QAction(
            'Import compounds from database', self,
            triggered=self.import_db_rdk)
        self._add_prop_action = QtGui.QAction(
            'Add molecule properties', self,
            triggered=self.add_prop)
        self._add_drc_action = QtGui.QAction(
            'Add dose-response curve', self,
            triggered=self.add_drc)
        self._export_action = QtGui.QAction(
            'Export to Excel worksheet', self,
            triggered=self.export)
        self._copy_action = QtGui.QAction(
            "&Copy", self,
            shortcut=QtGui.QKeySequence.Copy, triggered=self.copy)
        self._import_db_cdk_action = QtGui.QAction(
            'Import compounds from database(CDK)', self,
            triggered=self.import_db_cdk)
        self._import_sdf_action = QtGui.QAction(
            'Import compounds from SDFile', self,
            triggered=self.import_sdf)

        self._add_prop_action.setDisabled(True)
        self._add_drc_action.setDisabled(True)
        self._export_action.setDisabled(True)

    def _create_menus(self):
        filemenu = self.menuBar().addMenu("File")
        filemenu.addAction(self._import_db_action)
        filemenu.addAction(self._add_prop_action)
        filemenu.addAction(self._add_drc_action)
        filemenu.addAction(self._export_action)

        editmenu = self.menuBar().addMenu("Edit")
        editmenu.addAction(self._copy_action)

        demomenu = self.menuBar().addMenu("Demo")
        demomenu.addAction(self._import_db_cdk_action)
        demomenu.addAction(self._import_sdf_action)

    def import_db(self, renderer):
        """Import and display compound structure image on main window
        """
        dlg = dialog.ImportDb()
        dlg.exec_()
        (ids, db) = dlg.query
        if len(ids) == 0:
            return
        wait_dlg = dialog.Wait()
        try:
            count = self._ctrl.import_db(db, ids, renderer)
        except exception.SQLiteConnectionError:
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("Database Connection Error")
            msgbox.exec_()
            return
        except StandardError:
            print traceback.format_exc()
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("Unexpected Error")
            msgbox.exec_()
            return
        wait_dlg.close()
        if count > 0:
            self._maintab.update_tab(self._table)
            self._add_prop_action.setEnabled(True)
            self._add_drc_action.setEnabled(True)
            self._export_action.setEnabled(True)

    def import_db_cdk(self):
        self.import_db("CDK")

    def import_db_rdk(self):
        self.import_db("RDKit")

    def add_prop(self):
        """Add molecule properties"""
        self._ctrl.add_prop()
        self._maintab.update_tab(self._table, True)
        self._add_prop_action.setEnabled(False)

    def add_drc(self):
        """Get Logical Assay reports from Genedata Screener"""
        wait_dlg = dialog.Wait()
        try:
            lalist = self._ctrl.show_lalist()
        except exception.JavaConnectionError:
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("No Genedata Server Connection")
            msgbox.exec_()
            return
        except StandardError:
            print traceback.format_exc()
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("Unexpected Error")
            msgbox.exec_()
            return
        wait_dlg.close()
        dlg = dialog.AddDrc(lalist)
        dlg.exec_()
        if dlg.reportkey is None:
            return
        wait_dlg = dialog.Wait()
        try:
            self._ctrl.add_drc(dlg.reportkey, dlg.reportname, dlg.options)
        except exception.JavaConnectionError:
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("No Genedata Server Connection")
            msgbox.exec_()
            return
        except StandardError:
            print traceback.format_exc()
            wait_dlg.close()
            msgbox = QtGui.QMessageBox()
            msgbox.setText("Unexpected Error")
            msgbox.exec_()
            return
        wait_dlg.close()
        self._maintab.update_tab(self._table, True)

    def import_sdf(self):
        """Open sdfile and import data to data"""
        dlg = dialog.OpenFile()
        wait_dlg = dialog.Wait()
        cnt = self._ctrl.import_sdf(dlg.path)
        wait_dlg.close()
        if cnt > 0:
            self._maintab.update_tab(self._table, True)
            self._add_prop_action.setEnabled(True)
            self._export_action.setEnabled(True)

    def export(self):
        """Export data table to Excel worksheet"""
        dlg = dialog.SaveFile()
        wait_dlg = dialog.Wait()
        self._table.export_xlsx(dlg.path)
        wait_dlg.close()

    def copy(self):
        """Copy data (click Edit->copy or Ctrl+C)"""
        data = self._maintab.get_tabview_selected()
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(data)


class MainTab(QtGui.QTabWidget):
    """GUI main tab class"""

    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)
        self._strview = None
        self._tabview = None

    def update_tab(self, table, tabview=False):
        """Remove child tabs and add new tabs with compound data list

        Args:
          table: cheddar.data.table object
          tabview: If true, sets table view as a current widget.
        """
        self.clear()
        self._strview = StructureViewTab(table.dict_())
        self._tabview = TableViewTab(
            table.dict_(), table.column_names())
        self.addTab(self._strview, "Structure view")
        self.addTab(self._tabview, "Table view")
        if tabview:
            self.setCurrentWidget(self._tabview)

    def get_tabview_selected(self):
        """Get selected cells in table view as tab-separeted values.
        (for copy and paste multiple cells)
        """
        return self._tabview.get_selected()


class StructureViewTab(QtGui.QWidget):
    """GUI structure view tab class"""

    def __init__(self, dict_, parent=None):
        """ Show structure view tab

        Args:
          dict_: dict of data{0: {col1: val, col2: val, ...}, 1: {}, ...}
        """
        super(StructureViewTab, self).__init__(parent)
        innerwidget = QtGui.QWidget()
        innerlayout = QtGui.QGridLayout()
        # Add records to structure panes
        for i in range(len(dict_)):
            # ID label
            idlabel = QtGui.QLabel(dict_[i].get("ID", unicode(i)))
            # Structure label
            strlabel = QtGui.QLabel()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(str(dict_[i]["Structure"]), "png")
            strlabel.setPixmap(pixmap)
            # Compose a panel
            widget = QtGui.QWidget()
            layout = QtGui.QVBoxLayout()
            layout.addWidget(strlabel)
            layout.addWidget(idlabel)
            widget.setLayout(layout)
            # Add the panel to the widget
            row = math.floor(i / 3)
            col = i % 3
            innerlayout.addWidget(widget, row, col)
        innerwidget.setLayout(innerlayout)
        innerwidget.adjustSize()
        # Add structure view widget to the tab
        layout = QtGui.QHBoxLayout()
        scrollarea = QtGui.QScrollArea()
        scrollarea.setWidget(innerwidget)
        layout.addWidget(scrollarea)
        self.setLayout(layout)


class TableViewTab(QtGui.QWidget):
    """GUI table view tab class"""

    def __init__(self, dict_, col_names, parent=None):
        """Show table view tab

        Args:
          dict_: dict of data{0: {col1: val, col2: val, ...}, 1: {}, ...}
          col_names: list of columns
        """
        super(TableViewTab, self).__init__(parent)
        self._tablewidget = QtGui.QTableWidget(len(dict_), len(dict_[0]))
        # Header settings
        vheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Vertical)
        vheader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self._tablewidget.setVerticalHeader(vheader)
        hheader = QtGui.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self._tablewidget.setHorizontalHeader(hheader)
        self._tablewidget.setHorizontalHeaderLabels(col_names)
        # Add selected records to the table
        for i in range(len(dict_)):
            for j, col in enumerate(col_names):
                if isinstance(dict_[i][col], bytearray):
                    piclabel = QtGui.QLabel()
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(str(dict_[i][col]), "png")
                    pixmap = pixmap.scaledToHeight(
                        200, QtCore.Qt.SmoothTransformation)
                    piclabel.setPixmap(pixmap)
                    self._tablewidget.setCellWidget(i, j, piclabel)
                else:
                    item = QtGui.QTableWidgetItem(dict_[i][col])
                    self._tablewidget.setItem(i, j, item)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._tablewidget)
        self.setLayout(layout)

    def get_selected(self):
        """Get selected cells in table view as tab-separeted values.
        (for copy and paste multiple cells)
        """
        abmodel = self._tablewidget.model()
        list_ = self._tablewidget.selectionModel().selectedIndexes()
        list_.sort()
        if len(list_) < 1:
            return
        copy_table = ""
        for i, _ in enumerate(list_):
            copy_table += str(abmodel.data(list_[i]))
            if i < len(list_) - 1:
                if list_[i].row() == list_[i + 1].row():
                    copy_table += "\t"
                else:
                    copy_table += "\n"
        return copy_table


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
