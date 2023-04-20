import pandas as pd
from typing import List

from .file_data_model import FileDataModel


class DataModel:
    """Data model for converter"""

    def __init__(self):
        self.data_model: dict[str, FileDataModel] = {}

    def add_file_tables(
        self, path: str, view_tab_index: int, data: List[pd.DataFrame]
    ) -> None:
        """Add tables from PDF file if not in data model"""
        if self.data_model.get(path):
            return None
        file_data_model = FileDataModel(path, view_tab_index, data)
        self.data_model[path] = file_data_model

    def remove_file_tables(self, path: str) -> bool:
        """Remove tables belong to specific file"""
        if self.data_model.get(path, False):
            return False
        self.data_model.pop(path)
        return True

    def get_file_tables(self, file_path: str) -> FileDataModel | None:
        return self.data_model.get(file_path)

    def is_file_open(self, path: str) -> bool:
        """Check if file in collection"""
        return self.data_model.get(path)

    def clean_data_model(self) -> None:
        """Clean data model, remove all information"""
        self.data_model.clear()

    def seve_file_tables_to_xlsx(self, path: str, file_name: str) -> None:
        """Saves file tabs as excel document with sheets"""
        fdm: FileDataModel = self.data_model.get(path)
        if not fdm:
            return
        with pd.ExcelWriter(file_name) as writer:
            for idx, tab in enumerate(fdm.tabs):
                tab.tab.to_excel(
                    writer, sheet_name=f"Sheet {idx}", index=False
                )
                # TODO: use XlsxWriter for formatting cells
