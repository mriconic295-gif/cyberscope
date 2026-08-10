"""
=========================================================
CyberScope Constants
=========================================================
Author : Krunal Paliwal
=========================================================
"""

from pathlib import Path

# -------------------------------------------------------
# APPLICATION METADATA
# -------------------------------------------------------

APP_NAME = "CyberScope"
APP_VERSION = "2.0"
APP_AUTHOR = "Krunal Paliwal"
APP_DESCRIPTION = "Professional Website Intelligence Platform"

# -------------------------------------------------------
# ROOT PATH
# -------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# PROJECT DIRECTORIES
# -------------------------------------------------------

ASSETS_DIR = ROOT_DIR / "assets"
CONFIG_DIR = ROOT_DIR / "config"
GUI_DIR = ROOT_DIR / "gui"
MODULES_DIR = ROOT_DIR / "modules"
THEMES_DIR = ROOT_DIR / "themes"
UTILS_DIR = ROOT_DIR / "utils"
WORKERS_DIR = ROOT_DIR / "workers"
DATABASE_DIR = ROOT_DIR / "database"
REPORTS_DIR = ROOT_DIR / "reports"
LOGS_DIR = ROOT_DIR / "logs"
WIDGETS_DIR = ROOT_DIR / "widgets"

# -------------------------------------------------------
# ASSETS & ICONS
# -------------------------------------------------------

LOGO = ASSETS_DIR / "logo.png"
BACKGROUND = ASSETS_DIR / "background.png"
SPLASH = ASSETS_DIR / "splash.png"
LOADING = ASSETS_DIR / "loading.gif"

ICONS = ASSETS_DIR / "icons"
APP_ICON = LOGO if LOGO.exists() else (ICONS / "app.ico")

# -------------------------------------------------------
# DATABASE
# -------------------------------------------------------

DATABASE_NAME = DATABASE_DIR / "history.db"

# -------------------------------------------------------
# LOG FILE
# -------------------------------------------------------

LOG_FILE = LOGS_DIR / "cyberscope.log"

# -------------------------------------------------------
# REPORT DIRECTORY
# -------------------------------------------------------

EXPORT_DIR = ROOT_DIR / "exports"
SCREENSHOT_DIR = ROOT_DIR / "screenshots"

# -------------------------------------------------------
# NETWORK
# -------------------------------------------------------

DEFAULT_TIMEOUT = 20
MAX_REDIRECTS = 10
VERIFY_SSL = True

USER_AGENT = (
    "CyberScope/2.0 "
    "(AI WAPT & OSINT Analyzer)"
)

# -------------------------------------------------------
# THREADING
# -------------------------------------------------------

MAX_THREADS = 16
THREAD_TIMEOUT = 120

# -------------------------------------------------------
# SCAN LIMITS
# -------------------------------------------------------

MAX_PORT = 1024
MIN_PORT = 1

DNS_TIMEOUT = 8
WHOIS_TIMEOUT = 10
HTTP_TIMEOUT = 15
SSL_TIMEOUT = 15
SCREENSHOT_TIMEOUT = 30

# -------------------------------------------------------
# COLORS
# -------------------------------------------------------

PRIMARY_COLOR = "#00ff88"
SECONDARY_COLOR = "#00c96b"
SUCCESS_COLOR = "#32CD32"
WARNING_COLOR = "#FFC107"
ERROR_COLOR = "#FF3B30"
INFO_COLOR = "#00BFFF"

BACKGROUND_COLOR = "#0d1117"
CARD_COLOR = "#161b22"
SIDEBAR_COLOR = "#10151c"
TEXT_COLOR = "#FFFFFF"
SUBTEXT_COLOR = "#AAAAAA"
BORDER_COLOR = "#30363d"

# -------------------------------------------------------
# STATUS
# -------------------------------------------------------

STATUS_READY = "READY"
STATUS_RUNNING = "SCANNING..."
STATUS_FINISHED = "COMPLETED"
STATUS_FAILED = "FAILED"
STATUS_IDLE = "IDLE"

# -------------------------------------------------------
# RISK LEVELS
# -------------------------------------------------------

LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"

# -------------------------------------------------------
# EXPORT FORMATS
# -------------------------------------------------------

EXPORT_TYPES = [
    "PDF",
    "HTML",
    "JSON",
    "CSV"
]

# -------------------------------------------------------
# SUPPORTED DNS RECORDS
# -------------------------------------------------------

DNS_RECORDS = [
    "A",
    "AAAA",
    "MX",
    "TXT",
    "NS",
    "SOA",
    "CAA",
    "CNAME",
    "PTR",
    "SRV"
]

# -------------------------------------------------------
# HTTP METHODS
# -------------------------------------------------------

HTTP_METHODS = [
    "GET",
    "HEAD"
]

# -------------------------------------------------------
# DEFAULT WINDOW
# -------------------------------------------------------

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 950
MIN_WIDTH = 1280
MIN_HEIGHT = 720
