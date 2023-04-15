import pandas as pd
import numpy as np
import math
from PyQt6 import QtCore
from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import Qt, QModelIndex


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = self._data.columns
        self._d: np.ndarray = self._data.to_numpy()
        self._list = self._d.tolist()
        self.rows = len(data)

    def data(self, index: QModelIndex, role: int):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            row: int = index.row()
            column: int = index.column()
            cell = self._list[row][column]
            if isinstance(cell, str):
                return cell
            if math.isnan(cell):
                return ""
            return cell

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = ...
    ):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            # return f"Column {section + 1}"
            return self.columns[section]
        if (
            orientation == Qt.Orientation.Vertical
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return f"{section + 1}"

    def rowCount(self, index: QModelIndex):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index: QModelIndex):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data.columns)
