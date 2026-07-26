"""
=========================================================
CyberScope Settings
=========================================================
"""

from pathlib import Path

from version import APP_NAME, APP_VERSION

# =========================================================
# APPLICATION
# =========================================================

APPLICATION_NAME = APP_NAME
APPLICATION_VERSION = APP_VERSION

# =========================================================
# WINDOW
# =========================================================

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

MINIMUM_WIDTH = 1280
MINIMUM_HEIGHT = 720

FULLSCREEN = False

WINDOW_RADIUS = 10

# =========================================================
# THEME
# =========================================================

DEFAULT_THEME = "dark"

ENABLE_BLUR = True

ENABLE_SHADOW = True

ENABLE_ANIMATION = True

ENABLE_GLOW = True

ENABLE_SMOOTH_SCROLL = True

# =========================================================
# SIDEBAR
# =========================================================

SIDEBAR_WIDTH = 250

SIDEBAR_COLLAPSED = 70

SHOW_TOOLTIPS = True

# =========================================================
# DASHBOARD
# =========================================================

CARD_RADIUS = 12

CARD_SHADOW = True

REFRESH_INTERVAL = 1000

# =========================================================
# NETWORK
# =========================================================

REQUEST_TIMEOUT = 15

DNS_TIMEOUT = 8

WHOIS_TIMEOUT = 10

SSL_TIMEOUT = 15

HTTP_TIMEOUT = 15

RETRY_COUNT = 3

VERIFY_SSL = True

FOLLOW_REDIRECT = True

# =========================================================
# THREADING
# =========================================================

MAX_WORKERS = 16

ENABLE_MULTITHREADING = True

# =========================================================
# REPORTS
# =========================================================

AUTO_SAVE_REPORT = True

DEFAULT_EXPORT = "PDF"

EXPORT_SCREENSHOT = True

EXPORT_JSON = True

EXPORT_HTML = True

EXPORT_CSV = True

# =========================================================
# SCREENSHOT
# =========================================================

SCREENSHOT_WIDTH = 1600

SCREENSHOT_HEIGHT = 900

FULL_PAGE = True

# =========================================================
# RISK ENGINE
# =========================================================

ENABLE_AI_SUMMARY = True

ENABLE_RISK_SCORE = True

ENABLE_RECOMMENDATION = True

# =========================================================
# HISTORY
# =========================================================

SAVE_HISTORY = True

MAX_HISTORY = 1000

# =========================================================
# LOGGING
# =========================================================

ENABLE_LOGGING = True

LOG_LEVEL = "INFO"

# =========================================================
# CACHE
# =========================================================

ENABLE_CACHE = True

CACHE_TIMEOUT = 300

# =========================================================
# DATABASE
# =========================================================

DATABASE_NAME = "history.db"

# =========================================================
# FOLDERS
# =========================================================

EXPORT_FOLDER = Path("exports")

REPORT_FOLDER = Path("reports")

SCREENSHOT_FOLDER = Path("screenshots")

LOG_FOLDER = Path("logs")

# =========================================================
# STARTUP
# =========================================================

SHOW_SPLASH = True

SPLASH_TIME = 5000

SHOW_VERSION = True

# =========================================================
# SECURITY
# =========================================================

SAFE_MODE = True

ALLOW_LOCAL_SCAN = True

ALLOW_PORT_SCAN = True

ENABLE_SSL_ANALYSIS = True

ENABLE_HEADER_ANALYSIS = True

ENABLE_TECH_DETECTION = True

ENABLE_WHOIS = True

ENABLE_DNS = True

ENABLE_SCREENSHOT_CAPTURE = True
