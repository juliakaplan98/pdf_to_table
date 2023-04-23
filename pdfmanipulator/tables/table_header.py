from typing import List

from PyQt6.QtWidgets import QTableView, QMenu, QHeaderView, QMenu, QWidget
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
        selected_rows = self.get_selected_rows_indexes()
        self.tab_data_model.copy_rows_by_index(selected_rows)

    def past_rows(self):
        """Pasts copied rows"""
        selected_rows = self.get_selected_rows_indexes()
        self.tab_data_model.past_rows(selected_rows)
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
        selected_rows = self.get_selected_rows_indexes()
        self.tab_data_model.delete_row_by_index(selected_rows)
        self.update_tab_table()

    def clear_rows(self):
        """Clear rows context"""
        selected_rows = self.get_selected_rows_indexes()
        self.tab_data_model.clear_rows(selected_rows)
        self.update_tab_table()

    def cut_columns(self):
        """Cut row(s)"""
        self.copy_columns()
        self.delete_columns()

    def copy_columns(self):
        """Copy selected or current columns"""
        selected_columns = self.get_selected_columns_indexes()
        self.tab_data_model.copy_columns_by_index(selected_columns)

    def past_columns(self):
        """Pasts copied columns"""
        selected_columns = self.get_selected_columns_indexes()
        self.tab_data_model.past_columns(selected_columns)
        self.update_tab_table()

    def add_column_left(self) -> None:
        pass

    def add_column_right(self) -> None:
        pass

    def delete_columns(self) -> None:
        pass

    def clear_columns(self):
        self.a = EntryDialogBox()
        self.a.show()
        self.a.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        if self.a.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            print(self.a.val)
        print(self.a.val)


    def update_tab_table(self) -> None:
        """Update tab table with new data frame"""
        self.table_model = TableModel(self.tab_data_model)
        self.setModel(self.table_model)

    def get_selected_rows_indexes(self) -> List[int]:
        """Returns set of indexes selected or clicked row"""
        selected_rows = {cell.row() for cell in self.selectedIndexes()}
        if not selected_rows or self.v not in selected_rows:
            selected_rows = {self.v}
        return list(selected_rows)

    def get_selected_columns_indexes(self) -> List[int]:
        """Returns set of indexes selected or clicked columns"""
        selected_columns = {cell.column() for cell in self.selectedIndexes()}
        if not selected_columns or self.v not in selected_columns:
            selected_columns = {self.h}
        return list(selected_columns)
