import logging

logger = logging.getLogger(__name__)


class UIEventHandlers:
    def __init__(self, browser_window):
        self.browser_window = browser_window

    def update_tab_title(self, title, tab):
        index = self.browser_window.tabs.indexOf(tab)
        if index != -1:
            self.browser_window.tabs.setTabText(index, title)
        logger.info(f"Tab {index} title updated to {title}")

    def load_started(self):
        self.browser_window.progressbar.setValue(0)
        self.browser_window.progressbar.show()
        logger.info("Page load started")

    def update_progress(self, progress):
        self.browser_window.progressbar.setValue(progress)

    def load_finished(self, success):
        self.browser_window.progressbar.hide()
        logger.info(f"Page load finished with success {success}")
