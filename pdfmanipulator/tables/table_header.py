from typing import List

from PyQt6.QtWidgets import QTableView, QMenu, QHeaderView, QMenu, QWidget, QMessageBox
from PyQt6.QtGui import QAction, QPalette, QContextMenuEvent
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets
from pdfmanipulator.data_model.table_data_model import TabDataModel
from .table_model import TableModel
from .entry_dialog_box import EntryDialogBox

class TableHeaders(QWidget):
    def __init__(self):
        super().__init__()
        self.vertical_header: QHeaderView = self.verticalHeader()
        self.horizontal_header: QHeaderView = self.horizontalHeader()
        self.table_model: TableModel = None
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

    def on_context_menu_event_vertical(self, pos: QtCore.QPoint):
        """Horizontal header context menu"""
        self.h, self.v = self.get_row_col_index(pos)
        context_menu = QMenu(self)
        context_menu.addAction(self.cut_rows_act)
        context_menu.addAction(self.copy_rows_act)
        context_menu.addAction(self.past_rows_act)
        context_menu.addSeparator()
        context_menu.addAction(self.add_row_above_act)
        context_menu.addAction(self.add_row_below_act)
        context_menu.addAction(self.delete_row_act)
        context_menu.addAction(self.clear_row_act)
        context_menu.exec(self.mapToGlobal(pos))

    def on_context_menu_event_horizontal(self, pos: QtCore.QPoint):
        """Vertical header context menu"""
        self.h, self.v = self.get_row_col_index(pos)
        context_menu = QMenu(self)
        context_menu.addAction(self.cut_columns_act)
        context_menu.addAction(self.copy_columns_act)
        context_menu.addAction(self.past_columns_act)
        context_menu.addSeparator()
        context_menu.addAction(self.add_column_left_act)
        context_menu.addAction(self.add_column_right_act)
        context_menu.addAction(self.delete_columns_act)
        context_menu.addAction(self.clear_columns_act)
        context_menu.exec(self.mapToGlobal(pos))

    def createActions(self):
        """Create headers actions."""
        # Column context menu
        self.cut_columns_act = QAction("Cut", self)
        self.cut_columns_act.triggered.connect(self.cut_columns)

        self.copy_columns_act = QAction("Copy", self)
        self.copy_columns_act.triggered.connect(self.copy_columns)

        self.past_columns_act = QAction("Past")
        self.past_columns_act.triggered.connect(self.past_columns)

        self.add_column_left_act = QAction("Add Column Left", self)
        self.add_column_left_act.triggered.connect(self.add_column_left)

        self.add_column_right_act = QAction("Add Column Right", self)
        self.add_column_right_act.triggered.connect(self.add_column_right)

        self.delete_columns_act = QAction("Delete Column(s)", self)
        self.delete_columns_act.triggered.connect(self.delete_columns)

        self.clear_columns_act = QAction("Clear", self)
        self.clear_columns_act.triggered.connect(self.clear_columns)

        # Row context menu
        self.cut_rows_act = QAction("Cut", self)
        self.cut_rows_act.triggered.connect(self.cut_rows)

        self.copy_rows_act = QAction("Copy", self)
        self.copy_rows_act.triggered.connect(self.copy_rows)

        self.past_rows_act = QAction("Past")
        self.past_rows_act.triggered.connect(self.past_rows)

        self.add_row_above_act = QAction("Add Row Above", self)
        self.add_row_above_act.triggered.connect(self.add_row_above)

        self.add_row_below_act = QAction("Add Row Below", self)
        self.add_row_below_act.triggered.connect(self.add_row_below)

        self.delete_row_act = QAction("Delete Row(s)", self)
        self.delete_row_act.triggered.connect(self.delete_rows)

        self.clear_row_act = QAction("Clear", self)
        self.clear_row_act.triggered.connect(self.clear_rows)

    def cut_rows(self):
        """Cut row(s)"""
        self.copy_rows()
        self.delete_rows()

    def copy_rows(self):
        """Copy selected or current rows"""
        self.tab_data_model.copy_rows_by_index(self.selected_rows_indexes)

    def past_rows(self):
        """Pasts copied rows"""
        self.tab_data_model.past_rows(self.selected_rows_indexes)
        self.update_tab_table()

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
        self.tab_data_model.delete_row_by_index(self.selected_rows_indexes)
        self.update_tab_table()

    def clear_rows(self):
        """Clear rows context"""
        self.tab_data_model.clear_rows(self.selected_rows_indexes)
        self.update_tab_table()

    def cut_columns(self):
        """Cut row(s)"""
        self.copy_columns()
        self.delete_columns()

    def copy_columns(self):
        """Copy selected or current columns"""
        self.tab_data_model.copy_columns_by_index(self.selected_columns_indexes)

    def past_columns(self):
        """Pasts copied columns"""
        self.tab_data_model.past_columns(self.selected_columns_indexes)
        self.update_tab_table()

    def add_column_left(self) -> None:
        """ Creates new empty column on the left"""
        index = self.h
        self.add_column_by_index(index)

    def add_column_right(self) -> None:
        """ Creates new empty column on the right"""
        index = self.h + 1
        self.add_column_by_index(index)

    def add_column_by_index(self, index: int)->None:
        """ Adding column by index"""
        columns_name = self.tab_data_model.header
        dialog = EntryDialogBox(
            title="New Column Name",
            prompt="Please enter new column name.",
            text="text")
        dialog.exec()
        name = dialog.text
        if name in columns_name:
            QMessageBox.critical(
                self,
                "Column Name Exist",
                f"Name: '{name}' already exist.",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return
        self.tab_data_model.insert_empty_column(index, name)
        self.update_tab_table()

    def delete_columns(self) -> None:
        """ Delete selected columns"""
        self.tab_data_model.delete_columns(self.selected_columns_indexes)
        self.update_tab_table()

    def clear_columns(self):
        """ Clear selected columns"""
        self.tab_data_model.clean_columns_by_index(self.selected_columns_indexes)
        self.update_tab_table()

    def update_tab_table(self) -> None:
        """Update tab table with new data frame"""
        self.table_model = TableModel(self.tab_data_model)
        self.setModel(self.table_model)

    @property
    def selected_rows_indexes(self) -> List[int]:
        """Returns set of indexes selected or clicked row"""
        selected_rows = {cell.row() for cell in self.selectedIndexes()}
        if not selected_rows or self.v not in selected_rows:
            selected_rows = {self.v}
        return list(selected_rows)

    @property
    def selected_columns_indexes(self) -> List[int]:
        """Returns set of indexes selected or clicked columns"""
        selected_columns = {cell.column() for cell in self.selectedIndexes()}
        if not selected_columns or self.h not in selected_columns:
            selected_columns = {self.h}
        return list(selected_columns)
