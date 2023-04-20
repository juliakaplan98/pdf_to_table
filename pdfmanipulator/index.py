# main_window_template.py

import sys
import pandas as pd
from typing import List
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QHBoxLayout,
    QWidget,
    QTabWidget,
)

from PyQt6.QtCore import Qt


from .tables.table_widget import TableWidget
from .pdf_file.open_pdf_file import OpenPDF
from .show_file.show_file import get_web_view
from .menu_bar.action_tuple import MenuAction
from .menu_bar.menu_bar import MenuBar
from .data_model.data_model import DataModel
from .data_model.file_data_model import FileDataModel
from .data_model.table_data_model import TabDataModel

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
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        # Right side panel settings
        self.side_panel = QWidget()
        # Data model
        self.data_model = DataModel()
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
        view_tab_index = self.tab_bar.addTab(web_view, name)

        # Extract tables from pdf file
        pdf = OpenPDF(file_name)
        tables: List[pd.DataFrame] = pdf.get_pdf_tables()

        # Update data model with new file
        self.data_model.add_file_tables(file_name, view_tab_index, tables)
        file_data_model = self.data_model.get_file_tables(file_name)
        if not file_data_model:
            return
        for index, tbl in enumerate(file_data_model.tabs):
            table = TableWidget(tbl.tab)
            if table.rows:
                tab_index = self.tab_bar.addTab(table, str(index + 1))
                tbl.tab_index = tab_index
                self.tab_bar.setTabToolTip(tab_index, f"{file_name}-{index+1}")

    def get_file_name(self, file_name: str) -> str:
        """Returns name of the file without extension"""
        name = Path(file_name).name
        name = name[0 : name.index(".")]
        return name

    def close_file(self) -> None:
        """Delete all selected files"""
        file_names: list[str] = self.sp.get_selected_file()
        for file_name in file_names:
            fdm = self.data_model.get_file_tables(file_name)
            if not fdm:
                return
            for tab in reversed(fdm.tabs_indexes):
                self.tab_bar.removeTab(tab)
            self.tab_bar.removeTab(fdm.view_tab_index)
            self.data_model.remove_file_tables(file_name)
        self.sp.remove_selected_from_file_list()

    def close_all_files(self) -> None:
        """Removes all files from file list and all tabs"""
        self.sp.remove_all_files()
        self.tab_bar.clear()
        self.data_model.clean_data_model()

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
