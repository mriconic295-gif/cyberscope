"""
=========================================================
CyberScope Helpers
Author : Krunal Paliwal
Version : 2.0
=========================================================
"""

from __future__ import annotations

import re
import socket
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime


# ==========================================================
# URL HELPERS
# ==========================================================

class URLHelper:

    @staticmethod
    def normalize(target: str) -> str:

        target = target.strip()

        if not target.startswith(("http://", "https://")):
            target = "https://" + target

        return target

    @staticmethod
    def hostname(target: str) -> str:

        return urlparse(
            URLHelper.normalize(target)
        ).hostname or ""

    @staticmethod
    def valid(target: str) -> bool:

        try:
            socket.gethostbyname(
                URLHelper.hostname(target)
            )
            return True
        except Exception:
            return False


# ==========================================================
# FILE HELPERS
# ==========================================================

class FileHelper:

    @staticmethod
    def ensure_directory(path):

        Path(path).mkdir(
            parents=True,
            exist_ok=True
        )

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    @staticmethod
    def filename(prefix, extension):

        return f"{prefix}_{FileHelper.timestamp()}.{extension}"


# ==========================================================
# TEXT HELPERS
# ==========================================================

class TextHelper:

    @staticmethod
    def clean(text):

        if text is None:
            return ""

        return str(text).strip()

    @staticmethod
    def truncate(text, length=150):

        text = TextHelper.clean(text)

        if len(text) <= length:
            return text

        return text[:length] + "..."


# ==========================================================
# DOMAIN HELPERS
# ==========================================================

class DomainHelper:

    @staticmethod
    def is_ipv4(value):

        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

        return re.match(pattern, value) is not None

    @staticmethod
    def resolve(domain):

        try:
            return socket.gethostbyname(domain)

        except Exception:
            return None


# ==========================================================
# SIZE FORMATTER
# ==========================================================

class SizeHelper:

    @staticmethod
    def human(size):

        units = [

            "B",

            "KB",

            "MB",

            "GB",

            "TB"

        ]

        value = float(size)

        for unit in units:

            if value < 1024:

                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} PB"


# ==========================================================
# TIME FORMATTER
# ==========================================================

class TimeHelper:

    @staticmethod
    def now():

        return datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

    @staticmethod
    def current_date():

        return datetime.now().strftime(

            "%Y-%m-%d"

        )


# ==========================================================
# SYSTEM INFO
# ==========================================================

class SystemHelper:

    @staticmethod
    def hostname():

        return socket.gethostname()

    @staticmethod
    def local_ip():

        try:

            return socket.gethostbyname(

                socket.gethostname()

            )

        except Exception:

            return "Unknown"


# ==========================================================
# VERSION
# ==========================================================

HELPER_VERSION = "2.0"


if __name__ == "__main__":

    print(

        "CyberScope Helpers Ready"

    )
