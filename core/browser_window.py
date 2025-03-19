import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QPalette, QColor
from ui.ui_components import ThinProgressBar, FixedWidthTabBar, BrowserTab
from managers.profile_manager import ProfileManager
from ui.navigation_controller import NavigationController
from managers.shortcut_manager import ShortcutManager
from ui.ui_event_handlers import UIEventHandlers
from core.settings_window import SettingsWindow

logger = logging.getLogger(__name__)


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SearchTabs")
        self.setGeometry(100, 100, 1024, 768)

        # Set dark background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#191A1A"))
        self.setPalette(palette)

        logger.info("Initializing browser window")

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
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabWidget::tab-bar { left: 0; }
            QTabBar::tab { background: #191A1A; color: white; padding: 5px; }
            QTabBar::tab:selected { background: #2D2E2E; }
        """)

        # Create left corner buttons (Home and Add Tab)
        leftcorner = QWidget()
        leftlayout = QHBoxLayout(leftcorner)
        leftlayout.setContentsMargins(5, 0, 5, 0)
        leftlayout.setSpacing(2)

        # Set up navigation controller
        self.navigation_controller = NavigationController(self)

        # Home button
        self.homebutton = QPushButton("🏠") #use a house emoji for the button icon
        self.homebutton.setToolTip("Go to Perplexity.ai home")
        self.homebutton.clicked.connect(self.navigation_controller.go_home)
        self.homebutton.setStyleSheet("""
            QPushButton {
                background-color: #191A1A;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2D2E2E;
            }
        """)
        leftlayout.addWidget(self.homebutton)

        # Add Tab button
        self.addtabbutton = QPushButton("+") #use a plus text for the add tab icon
        self.addtabbutton.setToolTip("Add new tab")
        self.addtabbutton.clicked.connect(self.add_new_tab)
        self.addtabbutton.setStyleSheet("""
            QPushButton {
                background-color: #191A1A;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2D2E2E;
            }
        """)
        leftlayout.addWidget(self.addtabbutton)

        # Create right corner button (Settings)
        self.settingsbutton = QPushButton("⚙️") #use a gear emoji for the settings icon
        self.settingsbutton.setToolTip("Settings")
        self.settingsbutton.clicked.connect(self.showsettings)
        self.settingsbutton.setStyleSheet("""
            QPushButton {
                background-color: #191A1A;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2D2E2E;
            }
        """)

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

        # Create first tab
        self.add_new_tab()

        # Set up shortcuts
        self.shortcut_manager = ShortcutManager(self)

        # Settings
        self.confirm_close_tabs = True

        logger.info("Browser window initialization complete")

    def add_new_tab(self):
        newtab = BrowserTab(self.profile)
        index = self.tabs.addTab(newtab, "Loading...")
        self.tabs.setCurrentWidget(newtab)

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
