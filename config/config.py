"""
=========================================================
CyberScope Configuration Manager
=========================================================
Author : Krunal Paliwal
=========================================================
"""

from pathlib import Path
import json

from .settings import *

ROOT_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = ROOT_DIR / "config" / "config.json"


class ConfigManager:
    """
    CyberScope Configuration Manager
    """

    def __init__(self):
        self.config = {
            # -----------------------------
            # General
            # -----------------------------
            "theme": DEFAULT_THEME,
            "language": "English",
            "show_splash": SHOW_SPLASH,
            "window_width": WINDOW_WIDTH,
            "window_height": WINDOW_HEIGHT,

            # -----------------------------
            # Dashboard
            # -----------------------------
            "enable_animation": ENABLE_ANIMATION,
            "enable_shadow": ENABLE_SHADOW,
            "enable_glow": ENABLE_GLOW,
            "refresh_interval": REFRESH_INTERVAL,

            # -----------------------------
            # Scanner
            # -----------------------------
            "multithreading": ENABLE_MULTITHREADING,
            "max_workers": MAX_WORKERS,
            "request_timeout": REQUEST_TIMEOUT,
            "retry_count": RETRY_COUNT,
            "verify_ssl": VERIFY_SSL,

            # -----------------------------
            # Scan Modules
            # -----------------------------
            "dns": ENABLE_DNS,
            "whois": ENABLE_WHOIS,
            "ssl": ENABLE_SSL_ANALYSIS,
            "headers": ENABLE_HEADER_ANALYSIS,
            "technology": ENABLE_TECH_DETECTION,
            "screenshot": ENABLE_SCREENSHOT_CAPTURE,
            "risk_engine": ENABLE_RISK_SCORE,
            "ai_summary": ENABLE_AI_SUMMARY,

            # -----------------------------
            # Export
            # -----------------------------
            "auto_save": AUTO_SAVE_REPORT,
            "pdf": EXPORT_SCREENSHOT,
            "json": EXPORT_JSON,
            "html": EXPORT_HTML,
            "csv": EXPORT_CSV,

            # -----------------------------
            # History
            # -----------------------------
            "history": SAVE_HISTORY,
            "max_history": MAX_HISTORY,

            # -----------------------------
            # Logging
            # -----------------------------
            "logging": ENABLE_LOGGING,
            "log_level": LOG_LEVEL
        }

        self.load()

    def load(self):
        """
        Load configuration
        """

        if CONFIG_FILE.exists():

            try:

                with open(CONFIG_FILE, "r", encoding="utf-8") as f:

                    data = json.load(f)

                    self.config.update(data)

            except Exception:

                pass

        else:

            self.save()

    def save(self):
        """
        Save configuration
        """

        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:

            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):

        return self.config.get(key, default)

    def set(self, key, value):

        self.config[key] = value

        self.save()

    def update(self, dictionary):

        self.config.update(dictionary)

        self.save()

    def reset(self):

        if CONFIG_FILE.exists():

            CONFIG_FILE.unlink()

        self.__init__()


config = ConfigManager()
