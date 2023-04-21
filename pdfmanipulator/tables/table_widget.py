# table_widget.py
# TableWidget represents table inside of tab
# creates context menu

import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QTableView, QMenu, QHeaderView
from PyQt6.QtGui import QAction, QContextMenuEvent
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets

from pdfmanipulator.data_model.table_data_model import TabDataModel
from .table_model import TableModel
from .table_header import TableHeader


class TableWidget(QTableView):
    """TableWidget extends QTableView"""

    def __init__(self, tab: TabDataModel) -> None:
        super().__init__()
        self.tab = tab
        self.data_frame = self.tab.tab
        self.tmodel = TableModel(self.tab)
        self.rows = self.tmodel.rows
        self.setModel(self.tmodel)
        self.setMinimumHeight(500)
        self.createActions()
        self.setAlternatingRowColors(True)
        # Table Header
        # self.header = self.horizontalHeader()
        # self.header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.header.contextMenuEvent = self.test

        # self.header: QHeaderView = TableHeader(Qt.Orientation.Horizontal)
        # self.setHorizontalHeader(self.header)
        # self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.horizontalHeader().customContextMenuRequested.connect(
            self.on_customContextMenuRequested_hh
        )

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_customContextMenuRequested_hh(self, pos):
        menu = QtWidgets.QMenu()
        menu.addAction("Foo Action HH")
        a = self.horizontalHeader().mapToGlobal(pos)
        print(a)

    def contextMenuEvent(self, event: QContextMenuEvent):
        """Create context menu and additional actions."""
        a = self.selectedIndexes()
        c = a[0].column()
        v = a[0].row()

        i = self.currentIndex()
        # self.edit(i)
        context_menu = QMenu(self)
        context_menu.addAction(self.add_row_above_act)
        context_menu.addAction(self.add_row_below_act)
        context_menu.addSeparator()
        context_menu.addAction(self.add_col_before_act)
        context_menu.addAction(self.add_col_after_act)
        context_menu.addSeparator()
        context_menu.addAction(self.delete_row_act)
        context_menu.addAction(self.delete_col_act)
        context_menu.addSeparator()
        # Create actions specific to the context menu
        copy_act = context_menu.addAction("Copy")
        paste_act = context_menu.addAction("Paste")
        context_menu.addSeparator()
        context_menu.addAction(self.clear_table_act)
        # Execute the context_menu and return the action
        # selected. mapToGlobal() translates the position
        # of the window coordinates to the global screen
        # coordinates. This way we can detect if a right-click
        # occurred inside of the GUI and display the context
        # menu
        action = context_menu.exec(self.mapToGlobal(event.pos()))
        # Check for actions selected in the context menu that
        # were not created in the menu bar
        if action == copy_act:
            self.copyItem()
        if action == paste_act:
            self.pasteItem()

    def createActions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.quit_act = QAction("Quit", self)
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)
        # Create actions for Table menu
        self.add_row_above_act = QAction("Add Row Above", self)
        self.add_row_above_act.triggered.connect(self.addRowAbove)
        self.add_row_below_act = QAction("Add Row Below", self)
        self.add_row_below_act.triggered.connect(self.addRowBelow)
        self.add_col_before_act = QAction("Add Column Before", self)
        self.add_col_before_act.triggered.connect(self.addColumnBefore)
        self.add_col_after_act = QAction("Add Column After", self)
        self.add_col_after_act.triggered.connect(self.addColumnAfter)
        self.delete_row_act = QAction("Delete Row", self)
        self.delete_row_act.triggered.connect(self.deleteRow)
        self.delete_col_act = QAction("Delete Column", self)
        self.delete_col_act.triggered.connect(self.deleteColumn)
        self.clear_table_act = QAction("Clear All", self)
        self.clear_table_act.triggered.connect(self.clearTable)

    def addRowAbove(self):
        # i = self.currentIndex()
        a = self.selectedIndexes()
        # c = a[0].column()
        row = a[0].row()

        header = [col for col in self.tab.tab.head().columns]
        line = pd.DataFrame(
            {h: " " for h in header},
            index=[0],
        )
        self.tab.insert_row(line, row + 1)
        # self.tab.tab = pd.concat([line, self.tab.tab[:]]).reset_index(
        #     drop=True
        # )
        self.tmodel = TableModel(self.tab)
        self.setModel(self.tmodel)

    def addRowBelow(self):
        header = [col for col in self.tab.tab.head().columns]
        line = ["" for h in header]
        self.tab.tab.loc[len(self.tab.tab)] = line
        self.tmodel = TableModel(self.tab)
        self.setModel(self.tmodel)

    def addColumnBefore(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.insertColumn(current_col)

    def addColumnAfter(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.insertColumn(current_col + 1)

    def deleteRow(self):
        current_row = self.table_widget.currentRow()
        self.table_widget.removeRow(current_row)

    def deleteColumn(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.removeColumn(current_col)

    def clearTable(self):
        self.table_widget.clear()
