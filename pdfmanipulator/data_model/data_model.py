import pandas as pd
from typing import List
from pathlib import Path


class TabDataModel:
    """Tab data model with undo redo"""

    def __init__(self, tab: pd.DataFrame):
        self.tab_index: int = -1
        self.tab_label: str = ""
        self.undo_redo_index: int = 0
        self.deleted: bool = False
        self.undo_redo_stack: List[pd.DataFrame] = [tab]

    @property
    def tab_index(self) -> int:
        return self.__tab_index

    @tab_index.setter
    def tab_index(self, index: int) -> None:
        self.__tab_index = index

    @property
    def tab_label(self) -> str:
        return self.__tab_label

    @tab_label.setter
    def tab_label(self, label: str) -> None:
        self.__tab_label = label

    @property
    def deleted(self) -> bool:
        return self.__deleted

    @deleted.setter
    def deleted(self, deleted: bool) -> None:
        self.__deleted = deleted

    @property
    def tab(self) -> pd.DataFrame:
        return self.undo_redo_stack[self.undo_redo_index]

    def insert_row(self, line, index: int) -> None:
        """Insert line into index"""
        df: pd.DataFrame = self.undo_redo_stack[0].copy()
        new_line = pd.DataFrame(line, index=[index])
        new_df = pd.concat(
            [df.iloc[: index - 1], new_line, df.iloc[index - 1 :]]
        ).reset_index(drop=True)
        self.undo_redo_stack.insert(0, new_df)
        self.undo_redo_index = 0


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
            self.tabs.append(TabDataModel(df))

    def get_file_name(self, file_path: str) -> str:
        """Returns name of the file without extension"""
        name = Path(file_path).name
        name = name[0 : name.index(".")]
        return name

    @property
    def view_tab_index(self) -> int:
        self.__view_tab_index

    @view_tab_index.setter
    def view_tab_index(self, index: int) -> None:
        self.__view_tab_index = index


class DataModel:
    """Data model for converter"""

    def __init__(self):
        self.data_model: dict[str, FileDataModel] = {}

    def add_file_tables(
        self, path: str, view_tab_index: int, data: List[pd.DataFrame]
    ) -> FileDataModel | None:
        """Add tables from PDF file if not in data model"""
        if self.data_model.get(path):
            return None
        file_data_model = FileDataModel(path, view_tab_index, data)
        self.data_model[path] = file_data_model
        return file_data_model

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
        fdm: FileDataModel = self.data_model.get(path)
        if not fdm:
            return
        with pd.ExcelWriter(file_name) as writer:
            for idx, tab in enumerate(fdm.tabs):
                tab.to_excel(writer, sheet_name=f"Sheet {idx}", index=False)
                # TODO: use XlsxWriter for formatting cells
