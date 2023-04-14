import pandas as pd
from typing import List


class DataModel:
    """Data model for converter"""

    def __init__(self):
        self.data_model: dict[str, List[pd.DataFrame]] = {}

    def add_file_tables(self, path: str, data: List[pd.DataFrame]) -> bool:
        """Add tables from PDF file if not in data model"""
        if self.data_model.get(path):
            return False

        # if list(self.data_model.keys()).index(path) >= 0:
        #     return False
        self.data_model[path] = data
        return True

    def remove_file_tables(self, path: str) -> bool:
        """Remove tables belong to specific file"""
        if self.data_model.get(path, False):
            return False
        self.data_model.pop(path)
        return True

    def is_file_open(self, path: str) -> bool:
        """Check if file in collection"""
        return self.data_model.get(path)

    def clean_data_model(self) -> None:
        """Clean data model, remove all information"""
        self.data_model.clear()

    def seve_file_tables_to_xlsx(self, path: str, file_name: str) -> None:
        """Saves file tabs as excel document with sheets"""
        tabs: List[pd.DataFrame] = self.data_model.get(path)
        if len(tabs) == 0:
            return
        with pd.ExcelWriter(file_name) as writer:
            for idx, tab in enumerate(tabs):
                tab.to_excel(writer, sheet_name=f"Sheet {idx}", index=False)
