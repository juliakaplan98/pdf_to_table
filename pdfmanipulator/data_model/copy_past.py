from typing import List
from typing import Any
import pandas as pd


class CopyPast:
    __copied_rows: List[List[Any]] = None
    __copied_columns: pd.DataFrame = None
    __copied_rectangle: List[List[Any]] = None

    @classmethod
    def get_copied_rows(cls) -> List[List[Any]]:
        return cls.__copied_rows

    @classmethod
    def set_copied_rows(cls, copied_lines: List[List[Any]]):
        cls.__copied_rows = copied_lines

    @classmethod
    def get_copied_columns(cls) -> pd.DataFrame:
        return cls.__copied_columns

    @classmethod
    def set_copied_columns(cls, copied_columns: pd.DataFrame):
        cls.__copied_columns = copied_columns

    @classmethod
    def get_copied_rectangle(cls) -> List[List[Any]]:
        return cls.__copied_rectangle

    @classmethod
    def set_copied_rectangle(cls, copied_rectangle: List[List[Any]]):
        cls.__copied_rectangle = copied_rectangle
