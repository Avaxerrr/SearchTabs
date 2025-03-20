from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QCheckBox, QPushButton,
                               QFormLayout, QGroupBox, QRadioButton, QHBoxLayout)
from utils.log_terminal import LogTerminal
import logging


class SettingsWindow(QDialog):
    def __init__(self, browser_window):
        super().__init__()
        self.browserwindow = browser_window
        self.setWindowTitle("Settings")

        # Set a larger fixed size to accommodate all content comfortably
        self.setFixedSize(300, 600)

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

        self.confirm_close_tabs_checkbox = QCheckBox("Confirm Before Closing Multiple Tabs")
        self.confirm_close_tabs_checkbox.setChecked(self.browserwindow.confirm_close_tabs)

        self.alwaysontop_checkbox = QCheckBox("Always on Top")

        self.clearhistory_checkbox = QCheckBox("Clear History/Cache")

        general_layout.addWidget(self.confirm_close_tabs_checkbox)
        general_layout.addWidget(self.alwaysontop_checkbox)
        general_layout.addWidget(self.clearhistory_checkbox)
        general_layout.addStretch(1)  # Add stretch to push items to the top

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Theme Settings Group
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(10)  # Increase spacing between radio buttons

        # Theme radio buttons
        current_theme = self.browserwindow.theme_manager.get_current_theme()

        self.theme_system = QRadioButton("System")
        self.theme_system.setChecked(current_theme == "System")

        self.theme_light = QRadioButton("Light")
        self.theme_light.setChecked(current_theme == "Light")

        self.theme_dark = QRadioButton("Dark")
        self.theme_dark.setChecked(current_theme == "Dark")

        theme_layout.addWidget(self.theme_system)
        theme_layout.addWidget(self.theme_light)
        theme_layout.addWidget(self.theme_dark)
        theme_layout.addStretch(1)  # Add stretch to push items to the top

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Shortcuts Group - Improved layout
        shortcuts_group = QGroupBox("Essential Shortcuts")
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

        alwaysontop_shortcut = QLabel("Ctrl+Shift+T")
        alwaysontop_shortcut.setMinimumWidth(100)

        shortcuts_layout.addRow("Reload:", reload_shortcut)
        shortcuts_layout.addRow("Add New Tab:", addtab_shortcut)
        shortcuts_layout.addRow("Close Tab:", closetab_shortcut)
        shortcuts_layout.addRow("Switch Between Tabs:", switchtabs_shortcut)
        shortcuts_layout.addRow("Send to Tray:", sendtotray_shortcut)
        shortcuts_layout.addRow("Always on Top:", alwaysontop_shortcut)

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

    def save_settings(self):
        # Save general settings
        self.browserwindow.confirm_close_tabs = self.confirm_close_tabs_checkbox.isChecked()

        # Save theme settings
        if self.theme_light.isChecked():
            self.browserwindow.theme_manager.set_theme("Light")
        elif self.theme_dark.isChecked():
            self.browserwindow.theme_manager.set_theme("Dark")
        elif self.theme_system.isChecked():
            self.browserwindow.theme_manager.set_theme("System")

        # Apply the theme immediately
        self.browserwindow.apply_theme()

        logging.info("Settings saved!")
        self.close()
