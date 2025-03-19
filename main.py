import sys
from PySide6.QtWidgets import QApplication
from core.browser_window import BrowserWindow
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    window = BrowserWindow()
    window.show()
    logger.info("Application started")
    sys.exit(app.exec())
