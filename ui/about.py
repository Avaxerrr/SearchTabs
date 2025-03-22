from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame, QHBoxLayout
from PySide6.QtGui import QFont, QDesktopServices, QIcon, QPixmap
from PySide6.QtCore import Qt, QUrl


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SearchTabs 1.0 Beta")
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

        # Create a horizontal layout for author info and logo
        author_layout = QHBoxLayout()

        # Author and contact info
        author_info = QVBoxLayout()
        author_label = QLabel("Author: Avaxerrr")
        author_label.setFont(QFont("Arial", 14, QFont.Bold))
        if self.theme_colors:
            author_label.setStyleSheet(f"color: {self.theme_colors['text']};")
        author_info.addWidget(author_label)

        contact_label = QLabel(
            "Discord: avaxerrr\n"
            "Email: zonemaxq@gmail.com"
        )
        contact_label.setFont(QFont("Arial", 10))
        author_info.addWidget(contact_label)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("icons/final/logo_s.png")
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Add author info and logo to horizontal layout
        author_layout.addLayout(author_info)
        author_layout.addStretch()
        author_layout.addWidget(logo_label)

        # Add the horizontal layout to the main content layout
        content_layout.addLayout(author_layout)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("path/to/your/logo.png")
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)

        # Add author info and logo to horizontal layout
        author_layout.addLayout(author_info)
        author_layout.addWidget(logo_label, alignment=Qt.AlignRight)

        # Add the horizontal layout to the main content layout
        content_layout.addLayout(author_layout)

        # Add horizontal separator
        self.add_separator(content_layout)

        # App Description
        description_label = QLabel(
            "SearchTabs is a lightweight desktop wrapper application for Perplexity that brings tabbed browsing "
            "functionality to your research workflow. Built using Python with PySide6, this unofficial app allows "
            "you to conduct multiple research sessions simultaneously without the need to open a web browser or "
            "juggle between windows. Unlike the official Perplexity desktop application which limits users to a "
            "single session, SearchTabs enables seamless multitasking with its intuitive tab system - perfect for "
            "researchers, students, and professionals who need to explore multiple topics efficiently."
        )
        description_label.setWordWrap(True)
        description_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(description_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # Features
        features_title = QLabel("Features:")
        features_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(features_title)

        features_label = QLabel(
            "• Tabbed Interface: Unlike the official Perplexity desktop app, SearchTabs allows you to open multiple "
            "Perplexity sessions in tabs\n"
            "• Keyboard Shortcuts: Includes essential shortcuts for tab management and navigation\n"
            "• Theme Management: Supports light and dark themes with automatic detection"
        )
        features_label.setWordWrap(True)
        features_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(features_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # Known Limitations
        limitations_title = QLabel("Known Limitations:")
        limitations_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(limitations_title)

        limitations_label = QLabel(
            "• No Voice Search: Voice search functionality is not supported as it's only available in the official "
            "Perplexity desktop app and mobile versions, not in the web interface.\n"
            "• Rendering Issues: Users may experience occasional black screens when resizing the application window "
            "due to limitations in the Qt WebEngine. This issue is planned to be addressed in an upcoming release.\n"
            "• Platform Availability: Currently limited to Windows since I don't have Mac or Linux to package the "
            "app as of the moment.\n"
            "• Theme Synchronization: When changing the app theme to dark/light mode, Perplexity's interface does not "
            "automatically adjust. Users need to manually change the theme in Perplexity's settings."
        )
        limitations_label.setWordWrap(True)
        limitations_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(limitations_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # Development Roadmap
        roadmap_title = QLabel("Development Roadmap:")
        roadmap_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(roadmap_title)

        roadmap_label = QLabel(
            "Upcoming versions of SearchTabs aim to include the following features:\n"
            "• Find in Page: Ctrl+F functionality for searching content\n"
            "• System Tray Integration: Minimize to system tray for background operation\n"
            "• Always on Top: Option to keep the window above other applications\n"
            "• Enhanced Tab Management: Option to reopen previously closed tabs\n"
            "• UI Improvements: Draggable tabs and refined interface elements\n"
            "• Performance Optimization: Improved memory management and startup time\n"
            "• Cross-Platform Support: Extending availability to macOS and Linux"
        )
        roadmap_label.setWordWrap(True)
        roadmap_label.setFont(QFont("Arial", 10))
        content_layout.addWidget(roadmap_label)

        # Add horizontal separator
        self.add_separator(content_layout)

        # Disclaimer
        disclaimer_title = QLabel("Disclaimer:")
        disclaimer_title.setFont(QFont("Arial", 12, QFont.Bold))
        content_layout.addWidget(disclaimer_title)

        disclaimer_label = QLabel(
            "SearchTabs is not affiliated with, associated with, or endorsed by Perplexity AI. "
            "This is an unofficial application created to provide a tabbed interface for accessing "
            "Perplexity's web services. Users should comply with Perplexity's terms of service when using "
            "this application.\n\n"
            "The primary purpose of this application is to provide a tabbed interface for Perplexity's web services. "
            "All Perplexity content is accessed through their official website, and this application does not modify, "
            "store, or redistribute any of Perplexity's proprietary content or services."
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

        copyright_label = QLabel("Copyright (c) 2025 Avaxerrr")
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
