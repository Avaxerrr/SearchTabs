import logging
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QProgressBar, QTabBar, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

logger = logging.getLogger(__name__)

class ThinProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumHeight(1)
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
                max-height: 1px;
            }
            QProgressBar::chunk {
                background-color: #4285F4;
            }
        """)

    # Add this method to the ThinProgressBar class
    def update_theme(self, theme):
        """Update progress bar color based on theme"""
        if theme == "Light":
            self.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: transparent;
                    max-height: 2px;
                }
                QProgressBar::chunk {
                    background-color: #4285F4;
                }
            """)
        else:
            self.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: transparent;
                    max-height: 2px;
                }
                QProgressBar::chunk {
                    background-color: #4285F4;
                }
            """)


class FixedWidthTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)  # Don't expand tabs to fill the tab bar
        self.setElideMode(Qt.TextElideMode.ElideRight)  # Add ellipsis for text that doesn't fit

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        size.setWidth(200)  # Set fixed width to 200 pixels (adjust as needed)
        return size

class BrowserTab(QWidget):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.webview = QWebEngineView()
        page = QWebEnginePage(profile, self.webview)
        self.webview.setPage(page)
        self.webview.setUrl(QUrl("https://www.perplexity.ai"))
        self.webview.setStyleSheet("background-color: #191A1A;")
        layout.addWidget(self.webview)

        logger.info("New browser tab created")
