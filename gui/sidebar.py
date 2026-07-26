"""
=========================================================
CyberScope Sidebar
Professional Navigation Panel
Author : Krunal Paliwal
=========================================================
"""

from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)

from PySide6.QtGui import (
    QIcon
)

from config.constants import ICONS


class Sidebar(QWidget):

    pageChanged = Signal(str)

    def __init__(self):

        super().__init__()

        self.setObjectName("sidebar")

        self.setMinimumWidth(250)

        self.setMaximumWidth(250)

        self.buttons = {}

        self.build_ui()

    # ==================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(12,15,12,15)

        layout.setSpacing(8)

        # ------------------------------------------
        # LOGO
        # ------------------------------------------

        self.logo = QLabel("CYBERSCOPE")

        self.logo.setAlignment(Qt.AlignCenter)

        self.logo.setObjectName("titleLabel")

        layout.addWidget(self.logo)

        layout.addSpacing(20)

        # ------------------------------------------
        # MENU ITEMS
        # ------------------------------------------

        menu = [

            ("Dashboard","dashboard"),
            ("Overview","overview"),
            ("DNS Lookup","dns"),
            ("WHOIS","whois"),
            ("IP Lookup","ip"),
            ("GeoIP","geoip"),
            ("ASN Lookup","asn"),
            ("Reverse DNS","reverse_dns"),
            ("SSL Certificate","ssl"),
            ("HTTP Headers","headers"),
            ("Security Headers","security"),
            ("Technologies","technology"),
            ("CDN Detector","cdn"),
            ("WAF Detector","waf"),
            ("Performance","performance"),
            ("Screenshot","screenshot"),
            ("Reports","reports"),
            ("Settings","settings")

        ]

        for text,key in menu:

            button = QPushButton(text)

            button.setCursor(Qt.PointingHandCursor)

            button.setCheckable(True)

            button.setMinimumHeight(46)

            button.clicked.connect(
                lambda checked,
                value=key:
                self.change_page(value)
            )

            self.buttons[key]=button

            layout.addWidget(button)

        layout.addStretch()

        # ------------------------------------------
        # FOOTER
        # ------------------------------------------

        self.footer = QLabel(
            "CyberScope\nv2.0"
        )

        self.footer.setAlignment(Qt.AlignCenter)

        self.footer.setStyleSheet("""

            color:#8B949E;

            font-size:10px;

        """)

        layout.addWidget(self.footer)

        self.buttons["dashboard"].setChecked(True)

    # ==================================================

    def change_page(self,page):

        for btn in self.buttons.values():

            btn.setChecked(False)

        self.buttons[page].setChecked(True)

        self.pageChanged.emit(page)
