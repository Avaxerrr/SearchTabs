from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFormLayout, QGroupBox
from utils.log_terminal import LogTerminal
import logging

class SettingsWindow(QDialog):
    def __init__(self, browser_window):
        super().__init__()
        self.browserwindow = browser_window
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()
        
        # Center the settings window relative to the browser window
        parent_geometry = self.browserwindow.geometry()
        self_size = self.size()
        x = parent_geometry.x() + (parent_geometry.width() - self_size.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - self_size.height()) // 2
        self.move(x, y)

    def initUI(self):
        layout = QVBoxLayout()

        # General Settings Group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout()
        
        self.confirm_close_tabs_checkbox = QCheckBox("Confirm Before Closing Multiple Tabs")
        self.confirm_close_tabs_checkbox.setChecked(self.browserwindow.confirm_close_tabs)
        
        self.alwaysontop_checkbox = QCheckBox("Always on Top")
        
        self.clearhistory_checkbox = QCheckBox("Clear History/Cache")
        
        general_layout.addWidget(self.confirm_close_tabs_checkbox)
        general_layout.addWidget(self.alwaysontop_checkbox)
        general_layout.addWidget(self.clearhistory_checkbox)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Shortcuts Group
        shortcuts_group = QGroupBox("Essential Shortcuts")
        shortcuts_layout = QFormLayout()
        
        reload_shortcut = QLabel("Ctrl+R")
        addtab_shortcut = QLabel("Ctrl+T")
        closetab_shortcut = QLabel("Ctrl+W")
        switchtabs_shortcut = QLabel("Ctrl+Tab")
        sendtotray_shortcut = QLabel("Ctrl+Shift+M")
        alwaysontop_shortcut = QLabel("Ctrl+Shift+T")
        
        shortcuts_layout.addRow("Reload", reload_shortcut)
        shortcuts_layout.addRow("Add New Tab", addtab_shortcut)
        shortcuts_layout.addRow("Close Tab", closetab_shortcut)
        shortcuts_layout.addRow("Switch Between Tabs", switchtabs_shortcut)
        shortcuts_layout.addRow("Send to Tray", sendtotray_shortcut)
        shortcuts_layout.addRow("Always on Top", alwaysontop_shortcut)
        
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
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def show_log_terminal(self):
        """Show the log terminal window"""
        if not hasattr(self, 'log_terminal') or not self.log_terminal.isVisible():
            self.log_terminal = LogTerminal(self)

            # Connect to the application's logger
            # If you don't have a logger set up yet, add this to your browser_window.py:
            # self.logger = logging.getLogger('browser')
            # self.logger.setLevel(logging.INFO)

            # Get the root logger if no specific logger exists
            logger = getattr(self.browserwindow, 'logger', logging.getLogger())
            logger.addHandler(self.log_terminal.get_log_handler())

            self.log_terminal.show()
        else:
            self.log_terminal.activateWindow()
    
    def save_settings(self):
        self.browserwindow.confirm_close_tabs = self.confirm_close_tabs_checkbox.isChecked()
        print("Settings saved!")
        self.close()
