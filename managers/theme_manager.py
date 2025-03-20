from PySide6.QtCore import QObject, Signal, QSettings
from PySide6.QtGui import QPalette, QColor
import darkdetect
import threading


class ThemeManager(QObject):
    theme_changed = Signal(str)

    # Theme color definitions
    LIGHT_THEME = {
        "background": "#FCFCF9",
        "text": "#000000",
        "tab_background": "#FCFCF9",
        "tab_selected": "#E8E8E5",
        "button_hover": "#E8E8E5",
        "progressbar": "#4285F4"
    }

    DARK_THEME = {
        "background": "#191A1A",
        "text": "#FFFFFF",
        "tab_background": "#191A1A",
        "tab_selected": "#2D2E2E",
        "button_hover": "#2D2E2E",
        "progressbar": "#4285F4"
    }

    def __init__(self):
        super().__init__()
        self.settings = QSettings("SearchTabs", "Preferences")
        self.current_theme = self.settings.value("theme", "System")

        # Start theme listener if system theme is selected
        if self.current_theme == "System":
            self._start_theme_listener()

    def set_theme(self, theme):
        if theme in ["Light", "Dark", "System"]:
            old_theme = self.current_theme
            self.current_theme = theme
            self.settings.setValue("theme", theme)

            # Start or stop the theme listener based on selection
            if theme == "System" and old_theme != "System":
                self._start_theme_listener()

            self.theme_changed.emit(theme)

    def get_current_theme(self):
        return self.current_theme

    def get_effective_theme(self):
        """Returns the actual theme to use (resolves System to Light/Dark)"""
        if self.current_theme == "System":
            system_theme = darkdetect.theme()
            return system_theme if system_theme in ["Light", "Dark"] else "Dark"
        return self.current_theme

    def get_colors(self):
        """Returns the color dictionary for the current effective theme"""
        effective_theme = self.get_effective_theme()
        return self.LIGHT_THEME if effective_theme == "Light" else self.DARK_THEME

    def get_palette(self):
        """Returns a QPalette configured for the current theme"""
        colors = self.get_colors()
        palette = QPalette()

        if self.get_effective_theme() == "Light":
            palette.setColor(QPalette.Window, QColor(colors["background"]))
            palette.setColor(QPalette.WindowText, QColor(colors["text"]))
            palette.setColor(QPalette.Base, QColor(colors["background"]))
            palette.setColor(QPalette.Text, QColor(colors["text"]))
            palette.setColor(QPalette.Button, QColor(colors["background"]))
            palette.setColor(QPalette.ButtonText, QColor(colors["text"]))
        else:
            palette.setColor(QPalette.Window, QColor(colors["background"]))
            palette.setColor(QPalette.WindowText, QColor(colors["text"]))
            palette.setColor(QPalette.Base, QColor(colors["background"]))
            palette.setColor(QPalette.Text, QColor(colors["text"]))
            palette.setColor(QPalette.Button, QColor(colors["background"]))
            palette.setColor(QPalette.ButtonText, QColor(colors["text"]))

        return palette

    def get_stylesheet(self):
        """Returns a stylesheet with the current theme colors"""
        colors = self.get_colors()

        return f"""
            QTabWidget::pane {{ border: 0; }}
            QTabWidget::tab-bar {{ left: 0; }}
            QTabBar::tab {{ 
                background: {colors["tab_background"]}; 
                color: {colors["text"]}; 
                padding: 5px; 
            }}
            QTabBar::tab:selected {{ background: {colors["tab_selected"]}; }}

            QPushButton {{
                background-color: {colors["background"]};
                color: {colors["text"]};
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {colors["button_hover"]};
            }}
        """

    def get_settings_window_stylesheet(self):
        """Returns a stylesheet specifically for the settings window"""
        colors = self.get_colors()
        effective_theme = self.get_effective_theme()

        # Define different background colors for settings window
        if effective_theme == "Light":
            settings_bg = "#F0F0F0"  # Slightly darker than main background for light theme
            checkbox_bg = "#FFFFFF"
            checkbox_indicator_border = "#999999"
            checkbox_indicator_checked_bg = "#4285F4"
            radio_bg = "#FFFFFF"
            radio_indicator_border = "#999999"
            radio_indicator_checked_bg = "#4285F4"
            groupbox_border = "#CCCCCC"
        else:
            settings_bg = "#252525"  # Slightly lighter than main background for dark theme
            checkbox_bg = "#333333"
            checkbox_indicator_border = "#666666"
            checkbox_indicator_checked_bg = "#4285F4"
            radio_bg = "#333333"
            radio_indicator_border = "#666666"
            radio_indicator_checked_bg = "#4285F4"
            groupbox_border = "#444444"

        return f"""
            QDialog {{
                background-color: {settings_bg};
            }}

            QGroupBox {{
                font-weight: bold;
                border: 1px solid {groupbox_border};
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                color: {colors["text"]};
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }}

            QCheckBox {{
                color: {colors["text"]};
                spacing: 8px;
            }}

            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {checkbox_indicator_border};
                border-radius: 3px;
                background-color: {checkbox_bg};
            }}

            QCheckBox::indicator:checked {{
                background-color: {checkbox_indicator_checked_bg};
                border: 1px solid {checkbox_indicator_checked_bg};
                image: url(:/icons/check.png);
            }}

            QRadioButton {{
                color: {colors["text"]};
                spacing: 8px;
            }}

            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {radio_indicator_border};
                border-radius: 8px;
                background-color: {radio_bg};
            }}

            QRadioButton::indicator:checked {{
                background-color: {radio_indicator_checked_bg};
                border: 1px solid {radio_indicator_checked_bg};
                image: url(:/icons/radio_check.png);
            }}

            QLabel {{
                color: {colors["text"]};
            }}

            QPushButton {{
                background-color: {colors["button_hover"]};
                color: {colors["text"]};
                border: none;
                padding: 8px;
                border-radius: 4px;
            }}

            QPushButton:hover {{
                background-color: #4285F4;
            }}
        """

    def _start_theme_listener(self):
        """Start a background thread to listen for OS theme changes"""
        try:
            t = threading.Thread(target=darkdetect.listener, args=(self._on_system_theme_change,))
            t.daemon = True
            t.start()
        except Exception as e:
            print(f"Failed to start theme listener: {e}")

    def _on_system_theme_change(self, new_theme):
        """Called when OS theme changes"""
        if self.current_theme == "System":
            # Emit the signal to trigger UI updates
            self.theme_changed.emit("System")
