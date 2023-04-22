import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QTableView, QMenu, QHeaderView, QMenu, QWidget
from PyQt6.QtGui import QAction, QPalette, QContextMenuEvent
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets
from pdfmanipulator.data_model.table_data_model import TabDataModel
from .table_model import TableModel


class TableHeaders(QWidget):
    def __init__(self):
        super().__init__()
        self.vertical_header: QHeaderView = self.verticalHeader()
        self.horizontal_header: QHeaderView = self.horizontalHeader()
        self.horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.createActions1()

    def get_row_col_index(self, pos: QtCore.QPoint) -> tuple[int, int]:
        x = pos.x()
        y = pos.y()
        return (
            self.horizontal_header.logicalIndexAt(x),
            self.vertical_header.logicalIndexAt(y),
        )

    def on_context_menu_event_horizontal(self, pos: QtCore.QPoint):
        """Get column and row number"""
        self.h, self.v = self.get_row_col_index(pos)
        context_menu = QMenu(self)
        context_menu.addAction(self.add_col_before_act1)
        context_menu.addAction(self.add_col_after_act1)
        context_menu.addAction(self.delete_col_act1)
        context_menu.exec(self.mapToGlobal(pos))

    def on_context_menu_event_vertical(self, pos: QtCore.QPoint):
        self.h, self.v = self.get_row_col_index(pos)
        context_menu = QMenu(self)
        context_menu.addAction(self.add_row_above_act1)
        context_menu.addAction(self.add_row_below_act1)
        context_menu.addAction(self.delete_row_act1)
        context_menu.exec(self.mapToGlobal(pos))

    def createActions1(self):
        """Create headers actions."""
        self.add_col_before_act1 = QAction("Add Column Before", self)
        self.add_col_before_act1.triggered.connect(self.add_column_before1)

        self.add_col_after_act1 = QAction("Add Column After", self)
        self.add_col_after_act1.triggered.connect(self.add_column_after1)

        self.delete_col_act1 = QAction("Delete Column", self)
        self.delete_col_act1.triggered.connect(self.delete_column1)

        self.add_row_above_act1 = QAction("Add Row Above", self)
        self.add_row_above_act1.triggered.connect(self.add_row_above1)

        self.add_row_below_act1 = QAction("Add Row Below", self)
        self.add_row_below_act1.triggered.connect(self.add_row_below1)

        self.delete_row_act1 = QAction("Delete Row", self)
        self.delete_row_act1.triggered.connect(self.delete_row1)

    def add_row_above1(self):
        row = self.selectedIndexes()[0].row()
        self.tab_data_model.insert_empty_row(row + 1)
        self.table_model = TableModel(self.tab_data_model)
        self.setModel(self.table_model)

    def add_row_below1(self):
        row = self.selectedIndexes()[0].row()
        self.tab_data_model.insert_empty_row(row + 2)
        self.table_model = TableModel(self.tab_data_model)
        self.setModel(self.table_model)

    def delete_row1(self):
        pass

    def add_column_before1(self):
        pass

    def add_column_after1(self):
        pass

    def delete_column1(self):
        pass
