from PyQt6.QtWidgets import (QLabel, QLineEdit, QPushButton, QDialog)
from PyQt6.QtCore import Qt

class EntryDialogBox(QDialog):
    def __init__(self, title: str = "Title", prompt: str = "Prompt", text: str = ''):
        super().__init__()
        self.title = title
        self.prompt = prompt
        self.name_edit = QLineEdit(self)
        self.text = text
        self.name_edit.setText(self.text)
        self.initialize_ui()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.show()

    @property
    def text(self) -> str:
        """ Return text from edit line """
        return self.__text

    @text.setter
    def text(self, text: str)->None:
        """ Set text in edit line """
        self.__text = text

    def initialize_ui(self):
        """Set up the application's GUI."""
        self.setMaximumSize(280, 125)
        self.setWindowTitle(self.title)
        self.setup_main_window()

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        QLabel(self.prompt, self).move(15, 15)

        self.name_edit.resize(250, 20)
        self.name_edit.move(15, 50)

        clear_button = QPushButton("Clear", self)
        clear_button.move(115, 90)
        clear_button.clicked.connect(self.clear_text)

        accept_button = QPushButton("OK", self)
        accept_button.move(195, 90)
        accept_button.clicked.connect(self.accept_text)

    def clear_text(self):
        """Clear the QLineEdit input field."""
        self.name_edit.clear()

    def accept_text(self):
        """Accept the user's input in the QLineEdit
        widget and close the program."""
        self.text = self.name_edit.text()
        self.close()

