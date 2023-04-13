from typing import List

from PyQt6.QtWidgets import QMenuBar, QMenu, QMainWindow
from PyQt6.QtGui import QAction

from .action_tuple import MenuAction


class MenuBar(QMenuBar):
    """Application menu bar"""

    def __init__(
        self, main_window: QMainWindow, menu: dict[str, List[MenuAction]]
    ):
        super().__init__()
        self.main_window = main_window
        self.main_window.menuBar().setNativeMenuBar(False)
        self.menu_bar: QMenuBar = self.main_window.menuBar()
        self.create_menu(menu)

    def create_menu(self, menu: dict[str, List[MenuAction]]) -> None:
        """Create the application's menu bar."""
        for key, value in menu.items():
            top_menu: QMenu = self.menu_bar.addMenu(key)
            for action in value:
                name = action.name
                setattr(self.main_window, name, QAction(action.name))
                attr: QAction = getattr(self.main_window, name)
                attr.setShortcut(action.shortcut)
                attr.triggered.connect(action.connection)
                top_menu.addAction(attr)
