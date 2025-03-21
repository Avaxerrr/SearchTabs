import os
import logging
from PySide6.QtCore import QStandardPaths, QSettings
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


class ProfileManager:
    def __init__(self, browser_window):
        self.browser_window = browser_window

    def setup_profile(self):
        appdatapath = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        profilepath = os.path.join(appdatapath, "searchtabs_profile")
        profile = QWebEngineProfile("searchtabs_profile", self.browser_window)
        profile.setPersistentStoragePath(profilepath)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB cache
        logger.info(f"Profile set up with path {profilepath}")
        return profile

    def reset_browser_data(self):
        """Mark browser data for deletion on next startup"""
        confirmation = QMessageBox.question(
            self.browser_window,
            "Reset Browser Data",
            "This will clear all browsing data and log you out of websites. The app will need to restart. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            # Mark profile for deletion on next startup
            settings = QSettings("YourOrganization", "SearchTabs")
            settings.setValue("reset_profile", True)

            QMessageBox.information(
                self.browser_window,
                "Data Marked for Reset",
                "Browser data will be reset when the app restarts."
            )

            # Restart the application
            import sys
            import subprocess
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)