from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame
from PySide6.QtGui import QFont, QDesktopServices, QIcon
from PySide6.QtCore import Qt, QUrl


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SearchTabs")
        self.setFixedSize(500, 500)

        # Get theme colors from parent if available
        self.theme_colors = None
        if parent and hasattr(parent, 'browserwindow') and hasattr(parent.browserwindow, 'theme_manager'):
            self.theme_colors = parent.browserwindow.theme_manager.get_colors()
            self.setPalette(parent.browserwindow.theme_manager.get_palette())

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        # Apply modern scrollbar styling
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #2A2A2A;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #666666;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #808080;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Apply theme-based styling
        if self.theme_colors:
            content_widget.setStyleSheet(
                f"background-color: {self.theme_colors['background']}; color: {self.theme_colors['text']};")

        # Author Information with styled header
        author_label = QLabel("Author: Avaxerrr")
        author_label.setFont(QFont("Arial", 14, QFont.Bold))
        if self.theme_colors:
            author_label.setStyleSheet(f"color: {self.theme_colors['text']};")
        content_layout.addWidget(author_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # App Description
        description_label = QLabel(
            "SearchTabs is a lightweight desktop wrapper application for Perplexity with a feature-rich interface, "
            "built using PySide6 (Qt for Python).\n\n"
            "This unofficial app provides a more efficient way to use Perplexity, offering a potentially lower "
            "resource footprint compared to Electron-based alternatives."
        )
        description_label.setWordWrap(True)
        description_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(description_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # Disclaimer
        disclaimer_title = QLabel("Disclaimer:")
        disclaimer_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(disclaimer_title)

        disclaimer_label = QLabel(
            "SearchTabs is not affiliated with, associated with, or endorsed by Perplexity AI. "
            "This is an unofficial application created to provide a feature-rich interface for accessing "
            "Perplexity's web services. Users should comply with Perplexity's terms of service when using "
            "this application.\n\n"
            "The primary purpose of this application is to provide a feature-rich interface and potentially "
            "lower resource consumption compared to Electron-based alternatives. All Perplexity content is "
            "accessed through their official website, and this application does not modify, store, or "
            "redistribute any of Perplexity's proprietary content or services."
        )
        disclaimer_label.setWordWrap(True)
        disclaimer_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(disclaimer_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # License Information
        license_title = QLabel("License:")
        license_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(license_title)

        license_label = QLabel("MIT License")
        license_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(license_label)

        copyright_label = QLabel("Copyright (c) 2023 Avaxerrr")
        copyright_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(copyright_label)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

        # GitHub Link Button with improved styling
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 10, 20, 20)

        github_button = QPushButton("Visit GitHub Repository")
        github_button.setFont(QFont("Arial", 10, QFont.Bold))
        github_button.setCursor(Qt.PointingHandCursor)
        github_button.setMinimumHeight(40)

        # Apply theme-based styling to button
        if self.theme_colors:
            button_container.setStyleSheet(f"background-color: {self.theme_colors['background']};")
            github_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.theme_colors['button_hover']};
                    color: {self.theme_colors['text']};
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background-color: #4285F4;
                }}
            """)

        github_button.clicked.connect(self.open_github_repo)
        button_layout.addWidget(github_button)

        main_layout.addWidget(button_container)

        self.setLayout(main_layout)

    def add_separator(self, layout):
        """Add a themed horizontal separator line"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        if self.theme_colors:
            line.setStyleSheet(
                f"background-color: {self.theme_colors['button_hover']}; min-height: 1px; max-height: 1px;")
        layout.addWidget(line)

    def open_github_repo(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Avaxerrr/SearchTabs_Perplexity_Alternative"))
