import pandas as pd
import numpy as np
import math
from PyQt6 import QtCore
from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import Qt, QModelIndex

from .table_model import TableModel


class TableWidget(QTableView):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()
        self.data_frame = df
        self.model = TableModel(self.data_frame)
        self.rows = self.model.rows
        self.setModel(self.model)
        self.setMinimumHeight(500)
