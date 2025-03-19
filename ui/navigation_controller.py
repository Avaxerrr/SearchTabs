import logging
from PySide6.QtCore import QUrl

logger = logging.getLogger(__name__)


class NavigationController:
    def __init__(self, browser_window):
        self.browser_window = browser_window

    def go_home(self):
        currenttab = self.browser_window.tabs.currentWidget()
        if currenttab:
            currenttab.webview.setUrl(QUrl("https://www.perplexity.ai"))
        logger.info("Navigating to home page")

    def reload_page(self):
        currenttab = self.browser_window.tabs.currentWidget()
        if currenttab:
            currenttab.webview.reload()
        logger.info("Page reload triggered")
