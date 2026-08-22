"""
=========================================================
CyberScope
Sidebar Navigation Component

Author : Krunal Paliwal
=========================================================
"""

import os
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
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Load Icon if available in assets/icons
        if icon_name:
            icon_path = os.path.join("assets", "icons", f"{icon_name}.png")
            if not os.path.exists(icon_path):
                icon_path = os.path.join("assets", "icons", f"{icon_name}.svg")
            
            if os.path.exists(icon_path):
                self.setIcon(QIcon(icon_path))
                self.setIconSize(QSize(20, 20))

        # Modern Custom Styling
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 18px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                color: #A0AAB0;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #2A2E39;
                color: #FFFFFF;
            }
            QPushButton:checked {
                background-color: #00ADB5;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)


class Sidebar(QFrame):

    pageChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(230)
        self.setStyleSheet("QFrame#sidebar { background-color: #1A1C23; border-right: 1px solid #2A2E39; }")
        self.buttons = {}
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 15)
        layout.setSpacing(8)

        # Brand Title / Logo Header
        self.brandLabel = QLabel(APP_NAME)
        self.brandLabel.setObjectName("sidebarBrand")
        self.brandLabel.setAlignment(Qt.AlignCenter)
        self.brandLabel.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ADB5; margin-bottom: 10px;")
        layout.addWidget(self.brandLabel)

        layout.addSpacing(10)

        # Navigation Items (Name, Key/Icon Name)
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
            btn = SidebarButton(name, icon_name=key, parent=self)
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
        self.footerLabel.setStyleSheet("color: #6C757D; font-size: 12px;")
        layout.addWidget(self.footerLabel)

    def _on_button_click(self, page_key, clicked_btn):
        # Radio button selection behavior
        for btn in self.buttons.values():
            btn.setChecked(False)
        clicked_btn.setChecked(True)
        self.pageChanged.emit(page_key)

    def set_active_page(self, page_key):
        if page_key in self.buttons:
            self._on_button_click(page_key, self.buttons[page_key])
