"""
=========================================================
CyberScope
Professional Dashboard

Author : Krunal Paliwal
=========================================================
"""

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (

    QWidget,

    QLabel,

    QTextEdit,

    QVBoxLayout,

    QHBoxLayout,

    QGridLayout,

    QFrame,

    QGroupBox,

    QSizePolicy

)

from themes.animations import apply_shadow


# ==========================================================
# Info Card
# ==========================================================

class InfoCard(QFrame):

    def __init__(self, title, value="--"):

        super().__init__()

        self.setObjectName("infoCard")

        self.setMinimumHeight(110)

        apply_shadow(self)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(18,18,18,18)

        layout.setSpacing(6)

        self.title = QLabel(title)

        self.title.setObjectName("cardTitle")

        self.value = QLabel(value)

        self.value.setObjectName("cardValue")

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.value)

    def setValue(self, text):

        self.value.setText(str(text))


# ==========================================================
# Dashboard
# ==========================================================

class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()

    # ======================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(15)

        # --------------------------------------------------

        # TOP CARDS

        # --------------------------------------------------

        cardLayout = QGridLayout()

        cardLayout.setSpacing(15)

        self.targetCard = InfoCard(

            "Target",

            "--"

        )

        self.ipCard = InfoCard(

            "Real IP",

            "--"

        )

        self.riskCard = InfoCard(

            "Risk Score",

            "0 / 100"

        )

        self.responseCard = InfoCard(

            "Response Time",

            "--"

        )

        cardLayout.addWidget(

            self.targetCard,

            0,

            0

        )

        cardLayout.addWidget(

            self.ipCard,

            0,

            1

        )

        cardLayout.addWidget(

            self.riskCard,

            0,

            2

        )

        cardLayout.addWidget(

            self.responseCard,

            0,

            3

        )

        root.addLayout(

            cardLayout

        )

        # --------------------------------------------------

        # MAIN GRID

        # --------------------------------------------------

        self.grid = QGridLayout()

        self.grid.setSpacing(15)

        root.addLayout(

            self.grid

        )

        # --------------------------------------------------

        # LEFT PANEL

        # --------------------------------------------------

        self.infoPanel = QGroupBox(

            "Target Information"

        )

        self.infoLayout = QVBoxLayout(

            self.infoPanel

        )

        self.infoLayout.setSpacing(10)

        self.infoText = QTextEdit()

        self.infoText.setReadOnly(True)

        self.infoLayout.addWidget(

            self.infoText

        )

        # --------------------------------------------------

        # CENTER PANEL

        # --------------------------------------------------

        self.screenshotPanel = QGroupBox(

            "Website Screenshot"

        )

        shotLayout = QVBoxLayout(

            self.screenshotPanel

        )

        self.screenshotLabel = QLabel(

            "Screenshot Preview"

        )

        self.screenshotLabel.setAlignment(

            Qt.AlignCenter

        )

        self.screenshotLabel.setMinimumHeight(

            350

        )

        self.screenshotLabel.setObjectName(

            "screenshotBox"

        )

        shotLayout.addWidget(

            self.screenshotLabel

        )

        # --------------------------------------------------

        # RIGHT PANEL

        # --------------------------------------------------

        self.techPanel = QGroupBox(

            "Detected Technologies"

        )

        techLayout = QVBoxLayout(

            self.techPanel

        )

        self.techText = QTextEdit()

        self.techText.setReadOnly(True)

        techLayout.addWidget(

            self.techText

        )

        self.grid.addWidget(

            self.infoPanel,

            0,

            0

        )

        self.grid.addWidget(

            self.screenshotPanel,

            0,

            1

        )

        self.grid.addWidget(

            self.techPanel,

            0,

            2

        )
              # --------------------------------------------------
        # BOTTOM SECTION
        # --------------------------------------------------

        bottomLayout = QGridLayout()

        bottomLayout.setSpacing(15)

        root.addLayout(bottomLayout)

        # ==========================================
        # AI SUMMARY
        # ==========================================

        self.aiPanel = QGroupBox("AI Threat Summary")

        aiLayout = QVBoxLayout(self.aiPanel)

        self.ai_summary = QTextEdit()

        self.ai_summary.setReadOnly(True)

        self.ai_summary.setPlaceholderText(

            "AI analysis will appear here..."

        )

        aiLayout.addWidget(self.ai_summary)

        # ==========================================
        # TERMINAL
        # ==========================================

        self.terminalPanel = QGroupBox(

            "Live Scanner Log"

        )

        terminalLayout = QVBoxLayout(

            self.terminalPanel

        )

        self.terminal = QTextEdit()

        self.terminal.setReadOnly(True)

        self.terminal.setPlaceholderText(

            "[+] Waiting for scan..."

        )

        terminalLayout.addWidget(

            self.terminal

        )

        # ==========================================
        # DNS
        # ==========================================

        self.dnsPanel = QGroupBox(

            "DNS Records"

        )

        dnsLayout = QVBoxLayout(

            self.dnsPanel

        )

        self.dnsText = QTextEdit()

        self.dnsText.setReadOnly(True)

        dnsLayout.addWidget(

            self.dnsText

        )

        # ==========================================
        # WHOIS
        # ==========================================

        self.whoisPanel = QGroupBox(

            "WHOIS"

        )

        whoisLayout = QVBoxLayout(

            self.whoisPanel

        )

        self.whoisText = QTextEdit()

        self.whoisText.setReadOnly(True)

        whoisLayout.addWidget(

            self.whoisText

        )

        # ==========================================
        # SSL
        # ==========================================

        self.sslPanel = QGroupBox(

            "SSL Certificate"

        )

        sslLayout = QVBoxLayout(

            self.sslPanel

        )

        self.sslText = QTextEdit()

        self.sslText.setReadOnly(True)

        sslLayout.addWidget(

            self.sslText

        )

        # ==========================================
        # SECURITY HEADERS
        # ==========================================

        self.securityPanel = QGroupBox(

            "Security Headers"

        )

        securityLayout = QVBoxLayout(

            self.securityPanel

        )

        self.securityText = QTextEdit()

        self.securityText.setReadOnly(True)

        securityLayout.addWidget(

            self.securityText

        )

        # ==========================================
        # HTTP HEADERS
        # ==========================================

        self.headersPanel = QGroupBox(

            "HTTP Headers"

        )

        headersLayout = QVBoxLayout(

            self.headersPanel

        )

        self.headersText = QTextEdit()

        self.headersText.setReadOnly(True)

        headersLayout.addWidget(

            self.headersText
        )

        # ==========================================
        # GRID
        # ==========================================

        bottomLayout.addWidget(

            self.aiPanel,

            0,

            0

        )

        bottomLayout.addWidget(

            self.terminalPanel,

            0,

            1

        )

        bottomLayout.addWidget(

            self.dnsPanel,

            1,

            0

        )

        bottomLayout.addWidget(

            self.whoisPanel,

            1,

            1

        )

        bottomLayout.addWidget(

            self.sslPanel,

            2,

            0

        )

        bottomLayout.addWidget(

            self.securityPanel,

            2,

            1

        )

        bottomLayout.addWidget(

            self.headersPanel,

            3,

            0,

            1,

            2

        )

        # ==========================================
        # STRETCH
        # ==========================================

        root.addStretch()

    # ======================================================
    # LOG TERMINAL
    # ======================================================

    def log(self, text):

        self.terminal.append(

            text

        )

    # ======================================================
    # CLEAR TERMINAL
    # ======================================================

    def clear_terminal(self):

        self.terminal.clear()

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh(self):

        self.log(

            "[+] Dashboard Refreshed"

        )
          # ======================================================
    # TARGET INFORMATION
    # ======================================================

    def set_target(self, target):

        self.targetCard.setValue(target)

    # ======================================================
    # REAL IP
    # ======================================================

    def set_real_ip(self, ip):

        self.ipCard.setValue(ip)

    # ======================================================
    # RESPONSE TIME
    # ======================================================

    def set_response_time(self, value):

        self.responseCard.setValue(

            f"{value} ms"

        )

    # ======================================================
    # RISK SCORE
    # ======================================================

    def update_score(self, score):

        self.riskCard.setValue(

            f"{score}/100"

        )

    # ======================================================
    # SCREENSHOT
    # ======================================================

    def set_screenshot(self, image_path):

        from PySide6.QtGui import QPixmap

        pix = QPixmap(image_path)

        if pix.isNull():

            return

        self.screenshotLabel.setPixmap(

            pix.scaled(

                self.screenshotLabel.size(),

                Qt.KeepAspectRatio,

                Qt.SmoothTransformation

            )

        )

    # ======================================================
    # TARGET INFORMATION
    # ======================================================

    def set_information(self, text):

        self.infoText.setPlainText(text)

    # ======================================================
    # TECHNOLOGIES
    # ======================================================

    def set_technologies(self, data):

        if isinstance(data,list):

            self.techText.setPlainText(

                "\n".join(data)

            )

        else:

            self.techText.setPlainText(

                str(data)

            )

    # ======================================================
    # DNS
    # ======================================================

    def set_dns(self,data):

        self.dnsText.setPlainText(

            str(data)

        )

    # ======================================================
    # WHOIS
    # ======================================================

    def set_whois(self,data):

        self.whoisText.setPlainText(

            str(data)

        )

    # ======================================================
    # SSL
    # ======================================================

    def set_ssl(self,data):

        self.sslText.setPlainText(

            str(data)

        )

    # ======================================================
    # HTTP HEADERS
    # ======================================================

    def set_headers(self,data):

        self.headersText.setPlainText(

            str(data)

        )

    # ======================================================
    # SECURITY HEADERS
    # ======================================================

    def set_security_headers(self,data):

        self.securityText.setPlainText(

            str(data)

        )

    # ======================================================
    # AI SUMMARY
    # ======================================================

    def set_ai_summary(self,text):

        self.ai_summary.setPlainText(

            text

        )

    # ======================================================
    # CLEAR ALL
    # ======================================================

    def clear(self):

        self.targetCard.setValue("--")

        self.ipCard.setValue("--")

        self.responseCard.setValue("--")

        self.riskCard.setValue("0 / 100")

        self.infoText.clear()

        self.techText.clear()

        self.dnsText.clear()

        self.whoisText.clear()

        self.sslText.clear()

        self.headersText.clear()

        self.securityText.clear()

        self.ai_summary.clear()

        self.terminal.clear()

        self.screenshotLabel.setText(

            "Screenshot Preview"

        )

    # ======================================================
    # START SCAN
    # ======================================================

    def scan_started(self,target):

        self.clear()

        self.targetCard.setValue(

            target

        )

        self.log(

            f"[+] Target : {target}"

        )

        self.log(

            "[+] Starting reconnaissance..."

        )

    # ======================================================
    # SCAN COMPLETE
    # ======================================================

    def scan_completed(self):

        self.log(

            "[+] Scan Completed."

        )

    # ======================================================
    # SCAN ERROR
    # ======================================================

    def scan_error(self,error):

        self.log(

            f"[ERROR] {error}"

        )
          # ======================================================
    # GEO IP
    # ======================================================

    def set_geoip(self, data):

        self.log("[+] GeoIP Updated")

        self.infoText.append("\n========== GEO IP ==========\n")

        self.infoText.append(str(data))

    # ======================================================
    # ASN
    # ======================================================

    def set_asn(self, data):

        self.log("[+] ASN Information Loaded")

        self.infoText.append("\n========== ASN ==========\n")

        self.infoText.append(str(data))

    # ======================================================
    # REVERSE DNS
    # ======================================================

    def set_reverse_dns(self, data):

        self.infoText.append("\n========== REVERSE DNS ==========\n")

        self.infoText.append(str(data))

    # ======================================================
    # WAF
    # ======================================================

    def set_waf(self, data):

        self.techText.append(

            f"\nWAF : {data}"

        )

    # ======================================================
    # CDN
    # ======================================================

    def set_cdn(self, data):

        self.techText.append(

            f"\nCDN : {data}"

        )

    # ======================================================
    # ROBOTS
    # ======================================================

    def set_robots(self, data):

        self.infoText.append(

            "\n========== ROBOTS ==========\n"

        )

        self.infoText.append(str(data))

    # ======================================================
    # SITEMAP
    # ======================================================

    def set_sitemap(self, data):

        self.infoText.append(

            "\n========== SITEMAP ==========\n"

        )

        self.infoText.append(str(data))

    # ======================================================
    # PERFORMANCE
    # ======================================================

    def set_performance(self, data):

        self.log(

            f"[+] Performance : {data}"

        )

    # ======================================================
    # FAVICON
    # ======================================================

    def set_favicon(self, path):

        self.log(

            "[+] Favicon Loaded"

        )

    # ======================================================
    # EXPORT DATA
    # ======================================================

    def export_data(self):

        return {

            "target": self.targetCard.value.text(),

            "ip": self.ipCard.value.text(),

            "risk": self.riskCard.value.text(),

            "response": self.responseCard.value.text(),

            "dns": self.dnsText.toPlainText(),

            "whois": self.whoisText.toPlainText(),

            "ssl": self.sslText.toPlainText(),

            "headers": self.headersText.toPlainText(),

            "security_headers": self.securityText.toPlainText(),

            "technologies": self.techText.toPlainText(),

            "summary": self.ai_summary.toPlainText()

        }

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.clear()

        self.log(

            "[+] Dashboard Reset"

        )

    # ======================================================
    # STATUS
    # ======================================================

    def set_status(self, text):

        self.log(

            f"[STATUS] {text}"

        )

    # ======================================================
    # APPEND
    # ======================================================

    def append(self, text):

        self.log(text)

    # ======================================================
    # VERSION
    # ======================================================

    def version(self):

        return "CyberScope Dashboard v2"
