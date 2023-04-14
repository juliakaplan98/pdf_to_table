import pandas as pd
from typing import List


class DataModel:
    """Data model for converter"""

    def __init__(self):
        self.data_model: dict[str, List[pd.DataFrame]] = {}

    def add_file_tables(self, path: str, data: List[pd.DataFrame]) -> bool:
        """Add tables from PDF file if not in data model"""
        if path in self.data_model.keys():
            return False

        # if list(self.data_model.keys()).index(path) >= 0:
        #     return False
        self.data_model[path] = data
        return True

    def remove_file_tables(self, path: str) -> bool:
        """Remove tables belong to specific file"""
        if path not in self.data_model.keys():
            return False
        self.data_model.pop(path)
        return True

    def is_file_open(self, path: str) -> bool:
        """Check if file in collection"""
        return path in self.data_model.keys()

    def clean_data_model(self) -> None:
        """Clean data model, remove all information"""
        self.data_model.clear()
