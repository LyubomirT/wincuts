import sys
import csv
from PySide2.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                               QHeaderView, QAbstractItemView, QMenu, QAction)
from PySide2.QtCore import Qt, QEvent, QPoint
from PySide2.QtGui import QKeySequence

class CsvRunner(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowCount(1)
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(["Column 1"])
        self.setVerticalHeaderLabels(["Row 1"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.installEventFilter(self)
        self.filename = None
        self.createActions()
        self.createMenu()

    def createActions(self):
        self.openAction = QAction("&Open", self, shortcut=QKeySequence.Open,
                                  triggered=self.openFile)
        self.saveAction = QAction("&Save", self, shortcut=QKeySequence.Save,
                                  triggered=self.saveFile)
        self.saveAsAction = QAction("Save &As...", self,
                                    shortcut=QKeySequence.SaveAs,
                                    triggered=self.saveFileAs)
        self.addRowAction = QAction("Add Row", self, triggered=self.addRow)
        self.addColumnAction = QAction("Add Column", self, triggered=self.addColumn)
        self.deleteRowAction = QAction("Delete Row", self, triggered=self.deleteRow)
        self.deleteColumnAction = QAction("Delete Column", self, triggered=self.deleteColumn)

    def createMenu(self):
        self.menu = QMenu(self)
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.saveAsAction)
        self.menu.addSeparator()
        self.menu.addAction(self.addRowAction)
        self.menu.addAction(self.addColumnAction)
        self.menu.addAction(self.deleteRowAction)
        self.menu.addAction(self.deleteColumnAction)

    def showContextMenu(self, pos):
        self.menu.exec_(self.mapToGlobal(pos))

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress and source == self:
            if event.button() == Qt.LeftButton:
                self.editItem(self.itemAt(event.pos()))
            elif event.button() == Qt.RightButton:
                self.setCurrentItem(self.itemAt(event.pos()))
        return super().eventFilter(source, event)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "",
                                                  "CSV Files (*.csv)")
        if filename:
            self.filename = filename
            self.loadFile()

    def loadFile(self):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            self.setRowCount(len(data))
            self.setColumnCount(len(data[0]))
            for i, row in enumerate(data):
                for j, cell in enumerate(row):
                    self.setItem(i, j, QTableWidgetItem(cell))
            self.setHorizontalHeaderLabels(data[0])
            self.setVerticalHeaderLabels([f"Row {i+1}" for i in range(len(data))])

    def saveFile(self):
        if self.filename:
            self.writeFile()
        else:
            self.saveFileAs()

    def saveFileAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "",
                                                  "CSV Files (*.csv)")
        if filename:
            self.filename = filename
            self.writeFile()

    def writeFile(self):
        with open(self.filename, "w") as file:
            writer = csv.writer(file)
            data = []
            data.append(self.horizontalHeaderLabels())
            for i in range(self.rowCount()):
                row = []
                for j in range(self.columnCount()):
                    item = self.item(i, j)
                    if item:
                        row.append(item.text())
                    else:
                        row.append("")
                data.append(row)
            writer.writerows(data)

    def addRow(self):
        row = self.currentRow()
        self.insertRow(row + 1)
        self.setVerticalHeaderItem(row + 1, QTableWidgetItem(f"Row {row + 2}"))

    def addColumn(self):
        column = self.currentColumn()
        self.insertColumn(column + 1)
        self.setHorizontalHeaderItem(column + 1, QTableWidgetItem(f"Column {column + 2}"))

    def deleteRow(self):
        row = self.currentRow()
        self.removeRow(row)

    def deleteColumn(self):
        column = self.currentColumn()
        self.removeColumn(column)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    csvRunner = CsvRunner()
    csvRunner.setWindowTitle("CsvRunner")
    csvRunner.show()
    sys.exit(app.exec_())
