import pandas as pd
from typing import List
from pathlib import Path

from .table_data_model import TabDataModel


class FileDataModel:
    """Data model per file"""

    def __init__(
        self, path: str, view_tab_index: int, data_frames: List[pd.DataFrame]
    ):
        # Path or URL to the file
        self.path: str = path
        # Name of the file with no extension
        self.name: str = self.get_file_name(path)
        # View tab index
        self.view_tab_index: int = view_tab_index
        # Create list of tab data models
        self.tabs: List[TabDataModel] = []
        for df in data_frames:
            if len(df.index) > 0:
                self.tabs.append(TabDataModel(df))

    def get_file_name(self, file_path: str) -> str:
        """Returns name of the file without extension"""
        name = Path(file_path).name
        name = name[0 : name.index(".")]
        return name

    @property
    def view_tab_index(self) -> int:
        return self.__view_tab_index

    @view_tab_index.setter
    def view_tab_index(self, index: int) -> None:
        self.__view_tab_index = index

    @property
    def tabs_indexes(self) -> List[int]:
        return [tab.tab_index for tab in self.tabs]
