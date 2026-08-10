"""
=========================================================
CyberScope Theme Loader
Author : Krunal Paliwal
=========================================================
"""

from pathlib import Path

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication


class DarkTheme:
    """
    CyberScope Theme Manager
    """

    def __init__(self):

        self.root = Path(__file__).resolve().parent

        self.qss_file = self.root / "style.qss"

    def load_stylesheet(self):

        if self.qss_file.exists():

            return self.qss_file.read_text(encoding="utf-8")

        return ""

    def apply(self, app: QApplication):

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor("#0D1117"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))

        palette.setColor(QPalette.Base, QColor("#161B22"))
        palette.setColor(QPalette.AlternateBase, QColor("#1F2630"))

        palette.setColor(QPalette.ToolTipBase, QColor("#0D1117"))
        palette.setColor(QPalette.ToolTipText, QColor("#FFFFFF"))

        palette.setColor(QPalette.Text, QColor("#FFFFFF"))

        palette.setColor(QPalette.Button, QColor("#161B22"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))

        palette.setColor(QPalette.Highlight, QColor("#00FF88"))
        palette.setColor(QPalette.HighlightedText, QColor("#000000"))

        palette.setColor(QPalette.Link, QColor("#00FF88"))

        app.setPalette(palette)

        app.setStyleSheet(self.load_stylesheet())


theme = DarkTheme()
