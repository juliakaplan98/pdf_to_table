""" Button action tuple """
from typing import NamedTuple
from typing import Callable


class ButtonAction(NamedTuple):
    """Tuple to describe buttons action"""

    name: str
    connection: Callable
