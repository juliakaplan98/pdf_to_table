import pandas as pd
from typing import List
from typing import Set
from typing import Any


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

    # @tab.setter
    # def tab(self, df: pd.DataFrame) -> None:
    #     self.undo_redo_stack[self.undo_redo_index] = df

    def insert_empty_row(self, index: int) -> None:
        """Insert line into index"""
        current_tab = self.tab
        header = [col for col in current_tab.head().columns]
        line = pd.DataFrame(
            {h: " " for h in header},
            index=[0],
        )
        df: pd.DataFrame = current_tab.copy()
        new_df = pd.concat(
            [df.iloc[: index - 1], line, df.iloc[index - 1 :]]
        ).reset_index(drop=True)
        self.undo_redo_stack.insert(0, new_df)
        self.undo_redo_index = 0

    def delete_row_by_index(self, indexes: Set[int]) -> None:
        """Delete row(s) from data frame"""
        new_df: pd.DataFrame = self.tab.copy()
        new_df = new_df.drop(indexes).reset_index(drop=True)
        self.undo_redo_stack.insert(0, new_df)
        self.undo_redo_index = 0

    def copy_rows_by_index(self, indexes: Set[int]) -> List[List[Any]]:
        """Copy columns from data frame by index"""
        rows = [
            self.tab.loc[idx, :].values.flatten().tolist() for idx in indexes
        ]
        return rows
