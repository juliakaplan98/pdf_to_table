from typing import Set

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
        self.createActions()
        self.h, self.v = [0, 0]

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
        context_menu.addAction(self.add_col_before_act)
        context_menu.addAction(self.add_col_after_act)
        context_menu.addAction(self.delete_col_act)
        context_menu.exec(self.mapToGlobal(pos))

    def on_context_menu_event_vertical(self, pos: QtCore.QPoint):
        self.h, self.v = self.get_row_col_index(pos)
        context_menu = QMenu(self)
        context_menu.addAction(self.add_row_above_act)
        context_menu.addAction(self.add_row_below_act)
        context_menu.addAction(self.delete_row_act)
        context_menu.exec(self.mapToGlobal(pos))

    def createActions(self):
        """Create headers actions."""
        # Column context menu
        self.add_col_before_act = QAction("Add Column Before", self)
        self.add_col_before_act.triggered.connect(self.add_column_before)

        self.add_col_after_act = QAction("Add Column After", self)
        self.add_col_after_act.triggered.connect(self.add_column_after)

        self.delete_col_act = QAction("Delete Column", self)
        self.delete_col_act.triggered.connect(self.delete_column)

        # Row context menu
        self.add_row_above_act = QAction("Add Row Above", self)
        self.add_row_above_act.triggered.connect(self.add_row_above)

        self.add_row_below_act = QAction("Add Row Below", self)
        self.add_row_below_act.triggered.connect(self.add_row_below)

        self.delete_row_act = QAction("Delete Row(s)", self)
        self.delete_row_act.triggered.connect(self.delete_rows)

        self.copy_rows_act = QAction("Copy Row(s)", self)
        self.copy_rows_act.triggered.connect(self.copy_rows)

    def add_row_above(self) -> None:
        """Add empty row above clicked row"""
        self.tab_data_model.insert_empty_row(self.v + 1)
        self.update_tab_table()

    def add_row_below(self) -> None:
        """Add empty row below clicked row"""
        self.tab_data_model.insert_empty_row(self.v + 2)
        self.update_tab_table()

    def delete_rows(self) -> None:
        """Delete clicked row or rows selection"""
        selected_rows = self.get_selected_rows_indexes()
        self.tab_data_model.delete_row_by_index(selected_rows)
        self.update_tab_table()

    def copy_rows(self):
        """Copy selected or current rows"""
        pass

    def add_column_before(self) -> None:
        pass

    def add_column_after(self) -> None:
        pass

    def delete_column(self) -> None:
        pass

    def update_tab_table(self) -> None:
        """Update tab table with new data frame"""
        self.table_model = TableModel(self.tab_data_model)
        self.setModel(self.table_model)

    def get_selected_rows_indexes(self) -> Set[int]:
        """Returns set of indexes selected or clicked row"""
        selected_rows = {cell.row() for cell in self.selectedIndexes()}
        if not selected_rows or self.v not in selected_rows:
            selected_rows = {self.v}
        return selected_rows
