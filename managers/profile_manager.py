import os
import logging
from PySide6.QtCore import QStandardPaths
from PySide6.QtWebEngineCore import QWebEngineProfile

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
