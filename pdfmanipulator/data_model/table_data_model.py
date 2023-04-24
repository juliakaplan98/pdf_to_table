import pandas as pd
from typing import List
from typing import Set
from typing import Any

from .copy_past import CopyPast


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

    def insert_empty_row(
        self, index: int, update_undo: bool = True
    ) -> pd.DataFrame:
        """Insert line into index"""
        line = pd.DataFrame(
            {h: " " for h in self.header},
            index=[0],
        )
        new_df: pd.DataFrame = self.tab.copy()
        new_df = pd.concat(
            [new_df.iloc[: index - 1], line, new_df.iloc[index - 1 :]]
        ).reset_index(drop=True)
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)
        return new_df

    def delete_row_by_index(
        self, indexes: List[int], update_undo: bool = True
    ) -> pd.DataFrame:
        """Delete row(s) from data frame"""
        new_df: pd.DataFrame = self.tab.copy()
        new_df = new_df.drop(indexes).reset_index(drop=True)
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)
        return new_df

    def copy_rows_by_index(self, indexes: List[int]) -> List[List[Any]]:
        """Copy rows from data frame by index"""
        rows = [
            self.tab.loc[idx, :].values.flatten().tolist() for idx in indexes
        ]
        CopyPast.set_copied_rows(rows)
        return rows

    def clear_rows(
        self, indexes: List[int], update_undo: bool = True
    ) -> pd.DataFrame:
        """Clear context of the rows"""
        new_df: pd.DataFrame = self.tab.copy()
        line = ["" for i in range(0, len(new_df.columns))]
        for idx in indexes:
            new_df.iloc[idx, 0:] = line
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)
        return new_df

    def past_rows(
        self, indexes: List[int], update_undo: bool = True
    ) -> pd.DataFrame:
        """Pasts rows from"""
        new_df = self.delete_row_by_index(indexes, False)
        lines = pd.DataFrame(CopyPast.get_copied_rows())
        old_header = list(lines)
        new_header = list(new_df)
        lines = lines.rename(
            columns={old: new for old, new in zip(old_header, new_header)}
        )
        index = indexes[0]
        new_df = pd.concat(
            [new_df.iloc[:index], lines, new_df.iloc[index:]]
        ).reset_index(drop=True)
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)
        return new_df

    def copy_columns_by_index(self, indexes: List[int]) -> List[List[Any]]:
        """Copy columns from data frame by index"""
        header = list(self.tab.head())
        columns = self.tab[[header[i] for i in indexes]]
        CopyPast.set_copied_columns(columns)
        return columns

    def past_columns(self, indexes: List[int]) -> None:
        pass

    def insert_empty_column(self, index, name, update_undo: bool = True):
        """ Insert empty column with name """
        new_df = self.tab.copy()
        new_df.insert(loc=index, column=name, value=" ")
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)

    def delete_columns(self, indexes: List[int], update_undo: bool = True)->None:
        """ Delete selected columns """
        columns = [self.header[i] for i in indexes]
        new_df = self.tab.copy()
        new_df = new_df.drop(columns=columns)
        if update_undo:
            self.add_new_dataframe_in_undo_redo(new_df)

    def add_new_dataframe_in_undo_redo(self, new_df: pd.DataFrame) -> None:
        """Add new dataframe in undo redo"""
        self.undo_redo_stack.insert(0, new_df)
        self.undo_redo_index = 0

    def get_copied_rows(self) -> List[List[Any]]:
        return CopyPast.get_copied_rows()

    @property
    def header(self) -> List[str]:
        """ Return header of current data frame as list"""
        header = [col for col in self.tab.head().columns]
        return header

