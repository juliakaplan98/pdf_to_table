import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QTableView, QMenu, QHeaderView
from PyQt6.QtGui import QAction, QPalette
from PyQt6.QtCore import Qt

from pdfmanipulator.data_model.table_data_model import TabDataModel
from .table_model import TableModel


class TableHeader(QHeaderView):
    def __init__(self, position: Qt.Orientation) -> None:
        super().__init__(position)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.set

    def contextMenuEvent(self, event):
        """Create context menu and additional actions."""
        a = self.tv.currentIndex()
        print(a.column())
        print(a.row())

        print(self.count())
        print(self.currentIndex().column())

    def flags(self, index):
        """Flags to make cell editable"""
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )
