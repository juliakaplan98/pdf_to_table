from typing import NamedTuple
from typing import Callable
from typing import List

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt

from .button_tuple import ButtonAction


class ButtonTuple(NamedTuple):
    name: str
    connection: Callable


class SidePanel:
    """Side panel for managing tabs and docs"""

    def __init__(self, side_panel: QWidget):
        self.side_panel = side_panel
        # Side vertical box
        self.side_v_box = QVBoxLayout()
        # File horizontal box
        self.file_h_box = QHBoxLayout()
        # Add buttons layout for file
        self.file_buttons_v_box = QVBoxLayout()
        # File list box
        self.file_list = self.get_file_list()

        self.initialize_panel()

    def initialize_panel(self) -> None:
        """initialize side panel"""
        self.side_panel.setFixedWidth(300)
        # Add vertical layout to side panel
        self.side_v_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_panel.setLayout(self.side_v_box)
        # Add file layout to side layout
        self.file_h_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.side_v_box.addLayout(self.file_h_box)
        # Add file list box to file layout
        self.file_h_box.addWidget(self.file_list)
        # Add file button layout
        self.file_buttons_v_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.file_h_box.addLayout(self.file_buttons_v_box)

    def get_file_list(self) -> QListWidget:
        """Create file list widget"""
        file_list = QListWidget()
        file_list.setFixedWidth(200)
        file_list.setFixedHeight(200)
        file_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        file_list.setAlternatingRowColors(True)
        return file_list

    def set_fille_buttons(
        self, file_dict: dict[str, List[ButtonAction]]
    ) -> None:
        file_buttons = file_dict["File"]
        for button in file_buttons:
            b = QPushButton(button.name)
            if button.connection:
                b.clicked.connect(button.connection)
            self.file_buttons_v_box.addWidget(b)

    def add_file_to_list(self, file_name: str) -> None:
        list_item = QListWidgetItem()
        list_item.setText(file_name)
        self.file_list.addItem(list_item)

    def get_selected_file(self) -> list[str]:
        selected: list[str] = [
            item.text() for item in self.file_list.selectedItems()
        ]
        return selected

    def remove_selected_from_file_list(self) -> None:
        selected_items: List[QListWidgetItem] = self.file_list.selectedItems()
        for selected_item in selected_items:
            self.file_list.takeItem(self.file_list.row(selected_item))

    def remove_all_files(self) -> None:
        """Removes all files from file list widget"""
        self.file_list.clear()
