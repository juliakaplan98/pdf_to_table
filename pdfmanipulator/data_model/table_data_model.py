import pandas as pd
from typing import List


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

    @tab.setter
    def tab(self, df: pd.DataFrame) -> None:
        self.undo_redo_stack[self.undo_redo_index] = df

    def insert_row(self, line, index: int) -> None:
        """Insert line into index"""
        df: pd.DataFrame = self.undo_redo_stack[0].copy()
        new_line = pd.DataFrame(line, index=[index])
        new_df = pd.concat(
            [df.iloc[: index - 1], line, df.iloc[index - 1 :]]
        ).reset_index(drop=True)
        self.undo_redo_stack.insert(0, new_df)
        self.undo_redo_index = 0
