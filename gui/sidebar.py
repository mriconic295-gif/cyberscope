"""
=========================================================
CyberScope Sidebar
Professional Navigation Panel
Author : Krunal Paliwal
=========================================================
"""

from PyQt5.QtCore import Qt, Signal

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)

from PyQt5.QtGui import (
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
        """
=========================================================
Sidebar Animation & Controls
=========================================================
"""

from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve
)

# ==================================================
# Collapse Sidebar
# ==================================================

    def collapse(self):

        self.animation = QPropertyAnimation(
            self,
            b"minimumWidth"
        )

        self.animation.setDuration(250)

        self.animation.setStartValue(250)

        self.animation.setEndValue(70)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.animation.start()

        self.setMaximumWidth(70)

        for button in self.buttons.values():

            button.setText("")

            button.setToolTip(
                button.objectName()
            )

    # ==================================================
    # Expand Sidebar
    # ==================================================

    def expand(self):

        self.animation = QPropertyAnimation(
            self,
            b"minimumWidth"
        )

        self.animation.setDuration(250)

        self.animation.setStartValue(70)

        self.animation.setEndValue(250)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.animation.start()

        self.setMaximumWidth(250)

        titles = {

            "dashboard":"Dashboard",
            "overview":"Overview",
            "dns":"DNS Lookup",
            "whois":"WHOIS",
            "ip":"IP Lookup",
            "geoip":"GeoIP",
            "asn":"ASN Lookup",
            "reverse_dns":"Reverse DNS",
            "ssl":"SSL Certificate",
            "headers":"HTTP Headers",
            "security":"Security Headers",
            "technology":"Technologies",
            "cdn":"CDN Detector",
            "waf":"WAF Detector",
            "performance":"Performance",
            "screenshot":"Screenshot",
            "reports":"Reports",
            "settings":"Settings"

        }

        for key, button in self.buttons.items():

            button.setText(
                titles[key]
            )

    # ==================================================
    # Toggle Sidebar
    # ==================================================

    def toggle(self):

        if self.minimumWidth() > 100:

            self.collapse()

        else:

            self.expand()

    # ==================================================
    # Select Page
    # ==================================================

    def set_active(self, page):

        if page not in self.buttons:

            return

        for btn in self.buttons.values():

            btn.setChecked(False)

        self.buttons[page].setChecked(True)

    # ==================================================
    # Enable / Disable
    # ==================================================

    def enable_all(self):

        for button in self.buttons.values():

            button.setEnabled(True)

    def disable_all(self):

        for button in self.buttons.values():

            button.setEnabled(False)

    # ==================================================
    # Current Page
    # ==================================================

    def current_page(self):

        for key, button in self.buttons.items():

            if button.isChecked():

                return key

        return "dashboard"

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.set_active("dashboard")

    # ==================================================
    # Update Footer
    # ==================================================

    def set_status(self, text):

        self.footer.setText(text)
