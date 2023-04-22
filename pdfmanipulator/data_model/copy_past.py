from typing import Set
from typing import List
from typing import Any


class CopyPast:
    __copied_rows: List[List[Any]] = None

    @classmethod
    @property
    def copied_rows(cls) -> List[List[Any]]:
        return cls.__copied_rows

    @classmethod
    @copied_rows.setter
    def copied_rows(cls, copied_lines: List[List[Any]]):
        __copied_rows = copied_lines
