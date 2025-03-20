import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from PySide6.QtGui import QPalette, QColor, QIcon
from ui.ui_components import ThinProgressBar, FixedWidthTabBar, BrowserTab
from managers.profile_manager import ProfileManager
from ui.navigation_controller import NavigationController
from managers.shortcut_manager import ShortcutManager
from managers.theme_manager import ThemeManager
from ui.ui_event_handlers import UIEventHandlers
from core.settings_window import SettingsWindow

logger = logging.getLogger(__name__)


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SearchTabs")

        # Set initial size
        self.resize(1024, 768)

        # Center the window on screen
        self.center_window()

        logger.info("Initializing browser window")

        # Set up theme manager
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self.apply_theme)

        # Set up profile manager
        self.profile_manager = ProfileManager(self)
        self.profile = self.profile_manager.setup_profile()

        # Create central widget with layout
        self.centralwidget = QWidget()
        self.mainlayout = QVBoxLayout(self.centralwidget)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)

        # Create tab widget with fixed width tabs
        self.tabs = QTabWidget()
        self.tabs.setTabBar(FixedWidthTabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Create left corner buttons (Home and Add Tab)
        leftcorner = QWidget()
        leftlayout = QHBoxLayout(leftcorner)
        leftlayout.setContentsMargins(5, 0, 5, 0)
        leftlayout.setSpacing(2)

        # Set up navigation controller
        self.navigation_controller = NavigationController(self)

        # Home button
        self.homebutton = QPushButton()
        self.homebutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("home")))
        self.homebutton.setToolTip("Go to Perplexity.ai home")
        self.homebutton.clicked.connect(self.navigation_controller.go_home)
        leftlayout.addWidget(self.homebutton)

        # Add Tab button
        self.addtabbutton = QPushButton()
        self.addtabbutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("add")))
        self.addtabbutton.setToolTip("Add new tab")
        self.addtabbutton.clicked.connect(self.add_new_tab)
        leftlayout.addWidget(self.addtabbutton)

        # Create right corner button (Settings)
        self.settingsbutton = QPushButton()
        self.settingsbutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("settings")))
        self.settingsbutton.setToolTip("Settings")
        self.settingsbutton.clicked.connect(self.showsettings)

        # Set corner widgets
        self.tabs.setCornerWidget(leftcorner, Qt.Corner.TopLeftCorner)
        self.tabs.setCornerWidget(self.settingsbutton, Qt.Corner.TopRightCorner)

        self.mainlayout.addWidget(self.tabs)

        # Create ultra-thin progress bar
        self.progressbar = ThinProgressBar()
        self.progressbar.hide()  # Hide initially
        self.mainlayout.addWidget(self.progressbar)

        self.setCentralWidget(self.centralwidget)

        # Set up UI event handlers
        self.ui_event_handlers = UIEventHandlers(self)

        # Apply theme before creating the first tab
        self.apply_theme(self.theme_manager.get_current_theme())

        # Create first tab
        self.add_new_tab()

        # Set up shortcuts
        self.shortcut_manager = ShortcutManager(self)

        # Settings
        self.confirm_close_tabs = True

        logger.info("Browser window initialization complete")

    def center_window(self):
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()

        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2

        # Move the window to the center
        self.move(x, y)

    def apply_theme(self, theme=None):
        """Apply the current theme to all UI elements"""
        logger.info(f"Applying theme: {theme if theme else self.theme_manager.get_current_theme()}")

        # Apply palette to main window
        self.setPalette(self.theme_manager.get_palette())

        # Apply stylesheet to tabs and buttons
        stylesheet = self.theme_manager.get_stylesheet()
        self.tabs.setStyleSheet(stylesheet)
        self.homebutton.setStyleSheet(stylesheet)
        self.addtabbutton.setStyleSheet(stylesheet)
        self.settingsbutton.setStyleSheet(stylesheet)

        # Update existing tabs
        colors = self.theme_manager.get_colors()
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, 'webview'):
                tab.webview.setStyleSheet(f"background-color: {colors['background']}")

        # Update progress bar
        self.progressbar.update_theme(self.theme_manager.get_effective_theme())

        self.homebutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("home")))
        self.addtabbutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("add")))
        self.settingsbutton.setIcon(QIcon(self.theme_manager.get_themed_icon_path("settings")))

    def add_new_tab(self):
        newtab = BrowserTab(self.profile)
        index = self.tabs.addTab(newtab, "Loading...")
        self.tabs.setCurrentWidget(newtab)

        # Apply theme to new tab
        colors = self.theme_manager.get_colors()
        newtab.webview.setStyleSheet(f"background-color: {colors['background']}")

        # Connect signals for tab title and loading progress
        newtab.webview.titleChanged.connect(
            lambda title, tab=newtab: self.ui_event_handlers.update_tab_title(title, tab))
        newtab.webview.loadStarted.connect(self.ui_event_handlers.load_started)
        newtab.webview.loadProgress.connect(self.ui_event_handlers.update_progress)
        newtab.webview.loadFinished.connect(self.ui_event_handlers.load_finished)

        logger.info("New tab added")

    def showsettings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec()

    def close_current_tab(self):
        currentindex = self.tabs.currentIndex()
        if currentindex != -1:
            self.close_tab(currentindex)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            logger.info(f"Tab {index} closed")
        else:
            logger.info("Cannot close last tab")
