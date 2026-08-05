"""
=========================================================
CyberScope
Sidebar Navigation Component

Author : Krunal Paliwal
=========================================================
"""

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy
)
from PyQt5.QtGui import QIcon
from config.constants import APP_NAME, APP_ICON


class SidebarButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


class Sidebar(QFrame):

    pageChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.buttons = {}
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(8)

        # Brand Title / Logo Header
        self.brandLabel = QLabel(APP_NAME)
        self.brandLabel.setObjectName("sidebarBrand")
        self.brandLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.brandLabel)

        layout.addSpacing(15)

        # Navigation Buttons List
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Network Recon", "network"),
            ("DNS Lookup", "dns"),
            ("SSL Analyzer", "ssl"),
            ("Headers Check", "headers"),
            ("Tech Detector", "tech"),
            ("AI Summary", "ai"),
            ("Settings", "settings")
        ]

        for name, key in nav_items:
            btn = SidebarButton(name, parent=self)
            btn.clicked.connect(lambda checked, k=key, b=btn: self._on_button_click(k, b))
            layout.addWidget(btn)
            self.buttons[key] = btn

        # Default Active Button
        if "dashboard" in self.buttons:
            self.buttons["dashboard"].setChecked(True)

        layout.addStretch()

        # Footer Info Label
        self.footerLabel = QLabel("CyberScope v2.0")
        self.footerLabel.setObjectName("sidebarFooter")
        self.footerLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.footerLabel)

    def _on_button_click(self, page_key, clicked_btn):
        # Uncheck other buttons for custom tab behavior
        for btn in self.buttons.values():
            if btn != clicked_btn:
                btn.setChecked(False)
        clicked_btn.setChecked(True)
        self.pageChanged.emit(page_key)

    def set_active_page(self, page_key):
        if page_key in self.buttons:
            self._on_button_click(page_key, self.buttons[page_key])
