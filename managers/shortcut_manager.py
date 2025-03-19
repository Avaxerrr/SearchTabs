import logging
from PySide6.QtGui import QShortcut, QKeySequence

logger = logging.getLogger(__name__)


class ShortcutManager:
    def __init__(self, browser_window):
        self.browser_window = browser_window
        self.setup_shortcuts()

    def setup_shortcuts(self):
        # New Tab shortcut (Ctrl+T)
        newtabshortcut = QShortcut(QKeySequence("Ctrl+T"), self.browser_window)
        newtabshortcut.activated.connect(self.browser_window.add_new_tab)

        # Reload shortcut (Ctrl+R)
        reloadshortcut = QShortcut(QKeySequence("Ctrl+R"), self.browser_window)
        reloadshortcut.activated.connect(self.browser_window.navigation_controller.reload_page)

        # Close Tab shortcut (Ctrl+W)
        closetabshortcut = QShortcut(QKeySequence("Ctrl+W"), self.browser_window)
        closetabshortcut.activated.connect(self.browser_window.close_current_tab)

        logger.info("Shortcuts configured")
