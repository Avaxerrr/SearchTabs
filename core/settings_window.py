from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QCheckBox, QPushButton,
                               QFormLayout, QGroupBox, QHBoxLayout, QComboBox)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from utils.log_terminal import LogTerminal
from ui.about import AboutDialog
import logging


class SettingsWindow(QDialog):
    def __init__(self, browser_window):
        super().__init__()
        self.browserwindow = browser_window
        self.setWindowTitle("Settings")

        # Set a larger fixed size to accommodate all content comfortably
        self.setFixedSize(300, 720)  # Increased height to accommodate new section

        # Apply current theme to settings window
        self.setPalette(self.browserwindow.theme_manager.get_palette())

        # Apply settings-specific stylesheet
        self.setStyleSheet(self.browserwindow.theme_manager.get_settings_window_stylesheet())

        self.initUI()

        # Center the settings window
        self.center_window()

    def center_window(self):
        # Get parent geometry
        parent_geometry = self.browserwindow.geometry()

        # Calculate the center point of the parent window
        parent_center_x = parent_geometry.x() + parent_geometry.width() // 2
        parent_center_y = parent_geometry.y() + parent_geometry.height() // 2

        # Calculate the position to place the settings window
        # so its center aligns with the parent window's center
        x = parent_center_x - (self.width() // 2)
        y = parent_center_y - (self.height() // 2)

        # Move the window to the center relative to parent
        self.move(x, y)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Increase spacing between major sections

        # General Settings Group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout()
        general_layout.setSpacing(10)  # Increase spacing between checkboxes

        self.confirm_close_tabs_checkbox = QCheckBox("Warning before closing")
        self.confirm_close_tabs_checkbox.setChecked(self.browserwindow.confirm_close_tabs)

        general_layout.addWidget(self.confirm_close_tabs_checkbox)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Privacy & Data Group
        privacy_group = QGroupBox("Privacy and Data")
        privacy_layout = QVBoxLayout()
        privacy_layout.setSpacing(10)

        self.reset_data_button = QPushButton("Reset Browser Data")
        self.reset_data_button.clicked.connect(self.reset_browser_data)

        # Add a small description label
        reset_description = QLabel("Clears all browsing data and logs you out of websites")
        reset_description.setWordWrap(True)
        reset_description.setStyleSheet("color: gray; font-size: 10px;")

        privacy_layout.addWidget(self.reset_data_button)
        privacy_layout.addWidget(reset_description)

        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)

        # Theme Settings Group
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QVBoxLayout()

        # Theme dropdown menu
        current_theme = self.browserwindow.theme_manager.get_current_theme()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])

        # Set current theme in dropdown
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        theme_layout.addWidget(self.theme_combo)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Shortcuts Group - Improved layout
        shortcuts_group = QGroupBox("App Shortcuts")
        shortcuts_layout = QFormLayout()
        shortcuts_layout.setSpacing(10)  # Increase spacing between rows
        shortcuts_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # Set minimum width for the shortcut labels to prevent text compression
        reload_shortcut = QLabel("Ctrl+R")
        reload_shortcut.setMinimumWidth(100)

        addtab_shortcut = QLabel("Ctrl+T")
        addtab_shortcut.setMinimumWidth(100)

        closetab_shortcut = QLabel("Ctrl+W")
        closetab_shortcut.setMinimumWidth(100)

        switchtabs_shortcut = QLabel("Ctrl+Tab")
        switchtabs_shortcut.setMinimumWidth(100)

        sendtotray_shortcut = QLabel("Ctrl+Shift+M")
        sendtotray_shortcut.setMinimumWidth(100)

        shortcuts_layout.addRow("Reload:", reload_shortcut)
        shortcuts_layout.addRow("Add New Tab:", addtab_shortcut)
        shortcuts_layout.addRow("Close Tab:", closetab_shortcut)
        shortcuts_layout.addRow("Switch Between Tabs:", switchtabs_shortcut)
        shortcuts_layout.addRow("Send to Tray:", sendtotray_shortcut)

        shortcuts_group.setLayout(shortcuts_layout)
        layout.addWidget(shortcuts_group)

        # Developer Tools Group
        dev_group = QGroupBox("Developer Tools")
        dev_layout = QVBoxLayout()

        self.log_terminal_button = QPushButton("Open Log Terminal")
        self.log_terminal_button.clicked.connect(self.show_log_terminal)

        dev_layout.addWidget(self.log_terminal_button)
        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)

        # About and Updates Group
        about_group = QGroupBox("About and Updates")
        about_layout = QVBoxLayout()
        about_layout.setSpacing(10)

        self.update_button = QPushButton("Check for Updates")
        self.update_button.clicked.connect(self.open_github_repo)

        self.about_button = QPushButton("About SearchTabs")
        self.about_button.clicked.connect(self.show_about_dialog)

        about_layout.addWidget(self.update_button)
        about_layout.addWidget(self.about_button)

        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        # Save Button
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)  # Add top margin

        save_button = QPushButton("Save Settings")
        save_button.setMinimumWidth(120)  # Set minimum width for buttons
        save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumWidth(120)  # Set minimum width for buttons
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        # Set layout margins
        layout.setContentsMargins(20, 20, 20, 20)  # Add padding around all edges

        self.setLayout(layout)

    def reset_browser_data(self):
        """Call the profile manager to reset browser data"""
        self.browserwindow.profile_manager.reset_browser_data()

    def show_log_terminal(self):
        """Show the log terminal window"""
        if not hasattr(self, 'log_terminal') or not self.log_terminal.isVisible():
            self.log_terminal = LogTerminal(self)

            # Get the root logger if no specific logger exists
            logger = getattr(self.browserwindow, 'logger', logging.getLogger())
            logger.addHandler(self.log_terminal.get_log_handler())

            self.log_terminal.show()
        else:
            self.log_terminal.activateWindow()

    def open_github_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Avaxerrr/SearchTabs_Perplexity_Alternative"))

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def save_settings(self):
        # Save general settings
        self.browserwindow.confirm_close_tabs = self.confirm_close_tabs_checkbox.isChecked()

        # Save theme settings
        selected_theme = self.theme_combo.currentText()
        self.browserwindow.theme_manager.set_theme(selected_theme)

        # Apply the theme immediately
        self.browserwindow.apply_theme()

        logging.info("Settings saved!")
        self.close()
