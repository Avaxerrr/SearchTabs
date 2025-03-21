import sys
import os
import shutil
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSettings, QStandardPaths
from core.browser_window import BrowserWindow
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

def delete_profile():
    appdatapath = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    profilepath = os.path.join(appdatapath, "searchtabs_profile")
    if os.path.exists(profilepath):
        try:
            shutil.rmtree(profilepath)
            logger.info(f"Profile directory removed: {profilepath}")
        except Exception as e:
            logger.error(f"Error removing profile directory: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = QSettings("YourOrganization", "SearchTabs")
    if settings.value("reset_profile", False, type=bool):
        delete_profile()
        settings.setValue("reset_profile", False)
        settings.sync()  # Ensure settings are saved immediately

    # Set the global application icon
    basedir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(basedir, "icons", "logo2.png")
    app.setWindowIcon(QIcon(icon_path))

    app.setStyle("Fusion")  # Use Fusion style for better dark theme support
    window = BrowserWindow()
    window.show()
    logger.info("Application started")
    sys.exit(app.exec())