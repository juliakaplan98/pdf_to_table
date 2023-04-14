# main_window_template.py

import sys
import pandas as pd
from typing import List
from typing import Set
from pathlib import Path

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
)
from PyQt6.QtCore import Qt

from .tables.pdf_table import TableWidget
from .pdf_file.open_pdf_file import OpenPDF
from .show_file.show_file import get_web_view
from .menu_bar.action_tuple import MenuAction
from .menu_bar.menu_bar import MenuBar
from .data_model.data_model import DataModel
from .side_panel.side_panel import SidePanel
from .side_panel.button_tuple import ButtonAction


class MainWindow(QMainWindow):
    """Main Window class, creates application window"""

    def __init__(self):
        """Constructor of main application window"""
        super().__init__()
        # Central widget top container for app
        self.central_widget = QWidget()
        # Main layout for app (horizontal)
        self.main_h_box = QHBoxLayout()
        # Left side tab widget for all doc's and table's
        self.tab_bar = QTabWidget()
        # Right side panel settings
        self.side_panel = QWidget()
        # Data model
        self.data_model = DataModel()

        self.file_dict: dict[str, List[int]] = {}

        self.initialize_ui()

    def initialize_ui(self) -> None:
        """Set up the application's GUI"""
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("PDF Tables converter")
        self.setup_main_window()
        MenuBar(self, self.config_menu_bar())
        # Initialize side panel
        self.sp = SidePanel(self.side_panel)
        self.sp.set_fille_buttons(self.config_side_buttons())

        self.show()

    def setup_main_window(self) -> None:
        """Create and arrange widgets in the main window."""
        self.main_h_box.addWidget(self.tab_bar)
        self.main_h_box.addWidget(self.side_panel)
        self.central_widget.setLayout(self.main_h_box)
        self.setCentralWidget(self.central_widget)

    def config_menu_bar(self) -> dict[str, List[MenuAction]]:
        """Describes menu bar actions"""
        menu_bar_dict: dict[str, List[MenuAction]] = {
            "File": [
                MenuAction("Open File...", "Ctrl+O", self.open_pdf_file),
                MenuAction("&Quit", "Ctrl+Q", self.close),
            ]
        }
        return menu_bar_dict

    def config_side_buttons(self):
        """Describes side panel buttons"""
        side_bar_buttons_dict: dict[str, List[ButtonAction]] = {
            "File": [
                ButtonAction("Open", self.open_pdf_file),
                ButtonAction("Save As...", self.seve_selected_fales_as),
                ButtonAction("Save All As...", self.save_all_files_as),
                ButtonAction("Close", self.close_file),
                ButtonAction("Close All", self.close_all_files),
            ]
        }
        return side_bar_buttons_dict

    def open_pdf_file(self) -> None:
        """Open Open File Dialog and return name of selected file"""
        # Open Open File Dialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "PDF Files (*.pdf)"
        )
        if self.data_model.is_file_open(file_name):
            return
        self.sp.add_file_to_list(file_name)
        # Create document viewer
        name = self.get_file_name(file_name)
        web_view = get_web_view(file_name)
        tab_index = self.tab_bar.addTab(web_view, name)
        self.file_dict[file_name] = list()
        self.file_dict[file_name].append(tab_index)
        # Extract tables from pdf file
        pdf = OpenPDF(file_name)
        tables: List = pdf.get_pdf_tables()
        # Update data model
        self.data_model.add_file_tables(file_name, tables)
        name = 0
        for tbl in tables:
            table = TableWidget(tbl)
            if table.rows:
                name += 1
                tab_index = self.tab_bar.addTab(table.table_view, str(name))
                self.file_dict[file_name].append(tab_index)

    def get_file_name(self, file_name: str) -> str:
        """Returns name of the file without extension"""
        name = Path(file_name).name
        name = name[0 : name.index(".")]
        return name

    def close_file(self) -> None:
        file_names: list[str] = self.sp.get_selected_file()
        for file_name in file_names:
            for tab in reversed(self.file_dict[file_name]):
                self.tab_bar.removeTab(tab)
            del self.file_dict[file_name]
            self.data_model.remove_file_tables(file_name)
        self.sp.remove_selected_from_file_list()

    def close_all_files(self) -> None:
        """Removes all files from file list and all tabs"""
        self.sp.remove_all_files()
        self.tab_bar.clear()
        self.data_model.clean_data_model()
        self.file_dict.clear()

    def seve_selected_fales_as(self) -> None:
        """Save selected files tabs as"""
        # Open Open File Dialog
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Excel Files (*.xlsx)"
        )
        selected = self.sp.get_selected_file()
        if len(selected) == 0:
            return
        for file in selected:
            self.data_model.seve_file_tables_to_xlsx(file, file_name)

    def save_all_files_as(self) -> None:
        pass


def main():
    """Main method, start point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
