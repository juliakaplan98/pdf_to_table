# table_model.py
# Implements QAbstractTableModel class

import pandas as pd
import numpy as np
from typing import Any
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex


class TableModel(QtCore.QAbstractTableModel):
    """implementation of QAbstractTableModel class"""

    def __init__(self, data: pd.DataFrame):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = self._data.columns
        self._d: np.ndarray = self._data.to_numpy()
        self._list = self._d.tolist()
        self.rows = len(data)

    @property
    def df(self):
        return self._data

    @df.setter
    def df(self, df):
        self.beginResetModel()
        self._data = df.copy()
        self.endResetModel()

    def flags(self, index):
        """Flags to make cell editable"""
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if (
                role == Qt.ItemDataRole.DisplayRole
                or role == Qt.ItemDataRole.EditRole
            ):
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = ...
    ) -> int | float | bool | None:
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
        """Returns the length of the outer list."""
        return self._data.shape[0]

    def columnCount(self, index: QModelIndex):
        """The following takes the first sub-list, and returns
        the length (only works if all rows are an equal length)"""
        return self._data.shape[1]
