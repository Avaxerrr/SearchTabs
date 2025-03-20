import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from core.browser_window import BrowserWindow
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the global application icon
    basedir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(basedir, "icons", "logo2.png")
    app.setWindowIcon(QIcon(icon_path))

    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    window = BrowserWindow()
    window.show()
    logger.info("Application started")
    sys.exit(app.exec())
