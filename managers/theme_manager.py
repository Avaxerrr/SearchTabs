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
