""" Menu bar action tuple """
from typing import NamedTuple
from typing import Callable


class MenuAction(NamedTuple):
    """Tuple to describe menu bar action"""

    name: str
    shortcut: str
    connection: Callable
