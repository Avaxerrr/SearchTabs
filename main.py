import sys
import os
import shutil

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSettings, QStandardPaths, Qt, QTimer
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

    # Set the global application icon
    basedir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(basedir, "icons/final", "logo_s.png")
    if not os.path.exists(icon_path):
        # Try alternative path for packaged application
        icon_path = os.path.join(os.path.dirname(sys.executable), "icons/final", "logo_s.png")
    app.setWindowIcon(QIcon(icon_path))

    # Create and show splash screen
    splash_path = os.path.join(basedir, "icons/final", "logo_s.png")
    if not os.path.exists(splash_path):
        splash_path = os.path.join(os.path.dirname(sys.executable), "icons/final", "logo_s.png")

    splash_pixmap = QPixmap(splash_path)
    # Resize if needed (adjust dimensions as appropriate for your logo)
    if splash_pixmap.width() > 400 or splash_pixmap.height() > 400:
        splash_pixmap = splash_pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()

    # Process events to make sure splash is displayed immediately
    app.processEvents()

    settings = QSettings("YourOrganization", "SearchTabs")
    if settings.value("reset_profile", False, type=bool):
        delete_profile()
        settings.setValue("reset_profile", False)
        settings.sync()  # Ensure settings are saved immediately

    app.setStyle("Fusion")  # Use Fusion style for better dark theme support

    # Create the main window but don't show it yet
    window = BrowserWindow()


    # Function to finish splash and show main window
    def finish_splash():
        splash.finish(window)
        window.show()
        logger.info("Application started")


    # Use a timer to display the splash for a minimum time (e.g., 1 second)
    # This ensures the splash is visible even if the app loads quickly
    QTimer.singleShot(1000, finish_splash)


    sys.exit(app.exec())