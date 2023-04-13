import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTabWidget,
)

from PyQt6.QtGui import QAction

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl


def get_web_view(file_name: str) -> QWebEngineView:
    web_view = QWebEngineView()
    web_view.settings().setAttribute(
        QWebEngineSettings.WebAttribute.PluginsEnabled, True
    )
    web_view.settings().setAttribute(
        QWebEngineSettings.WebAttribute.PdfViewerEnabled, True
    )

    url = QUrl.fromLocalFile(file_name)
    web_view.setUrl(url)
    web_view.setZoomFactor(1.0)
    return web_view
