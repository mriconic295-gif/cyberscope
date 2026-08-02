"""
=========================================================
CyberScope Professional UI Components
Author : Krunal Paliwal
Version : 2.0
=========================================================
"""

from __future__ import annotations

from PyQt5.QtCore import (
    Qt,
    QSize,
    QRectF,
    QPoint,
    Property,
    QEasingCurve,
    QPropertyAnimation,
    QParallelAnimationGroup
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QLinearGradient,
    QFont,
    QPainterPath,
    QPaintEvent
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QGraphicsDropShadowEffect,
    QProgressBar
)

# ==========================================================
# COLORS
# ==========================================================

PRIMARY = "#00BFFF"
SECONDARY = "#0f172a"
CARD = "#172033"
TEXT = "#FFFFFF"
TEXT2 = "#B8C7E0"
SUCCESS = "#00D26A"
WARNING = "#FFB020"
DANGER = "#FF4C4C"

# ==========================================================
# SHADOW
# ==========================================================

def apply_shadow(widget):

    shadow = QGraphicsDropShadowEffect()

    shadow.setBlurRadius(35)

    shadow.setOffset(0,8)

    shadow.setColor(

        QColor(

            0,

            191,

            255,

            120

        )

    )

    widget.setGraphicsEffect(shadow)


# ==========================================================
# BASE CARD
# ==========================================================

class BaseCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("BaseCard")

        self.setMinimumHeight(120)

        self.setSizePolicy(

            QSizePolicy.Expanding,

            QSizePolicy.Fixed

        )

        apply_shadow(self)

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(

            18,

            18,

            18,

            18

        )

        self.layout.setSpacing(10)


# ==========================================================
# TITLE LABEL
# ==========================================================

class TitleLabel(QLabel):

    def __init__(self,text):

        super().__init__(text)

        self.setFont(

            QFont(

                "Segoe UI",

                12,

                QFont.Bold

            )

        )

        self.setStyleSheet(

            f"""

            color:{TEXT};

            background:transparent;

            """

        )


# ==========================================================
# VALUE LABEL
# ==========================================================

class ValueLabel(QLabel):

    def __init__(self,text="--"):

        super().__init__(text)

        self.setFont(

            QFont(

                "Consolas",

                20,

                QFont.Bold

            )

        )

        self.setStyleSheet(

            f"""

            color:{PRIMARY};

            background:transparent;

            """

        )

    def setValue(self,value):

        self.setText(

            str(value)

        )


# ==========================================================
# GLOW BUTTON
# ==========================================================

class GlowButton(QPushButton):

    def __init__(self,text):

        super().__init__(text)

        self.setCursor(

            Qt.PointingHandCursor

        )

        self.setMinimumHeight(46)

        self.setMinimumWidth(170)

        self.setStyleSheet("""

QPushButton{

background:#00BFFF;

border:none;

border-radius:10px;

color:white;

font-size:13px;

font-weight:bold;

}

QPushButton:hover{

background:#22d3ee;

}

QPushButton:pressed{

background:#0284c7;

}

""")

        apply_shadow(self)

        self.animation = QPropertyAnimation(

            self,

            b"minimumHeight"

        )

        self.animation.setDuration(

            150

        )

        self.animation.setStartValue(

            46

        )

        self.animation.setEndValue(

            50

        )

        self.animation.setEasingCurve(

            QEasingCurve.OutCubic

        )

    def enterEvent(self,event):

        self.animation.setDirection(

            QPropertyAnimation.Forward

        )

        self.animation.start()

        super().enterEvent(event)

    def leaveEvent(self,event):

        self.animation.setDirection(

            QPropertyAnimation.Backward

        )

        self.animation.start()

        super().leaveEvent(event)
      # ==========================================================
# ICON BUTTON
# ==========================================================

class IconButton(QPushButton):

    def __init__(self, text="", icon=None):

        super().__init__(text)

        self.setCursor(Qt.PointingHandCursor)

        self.setMinimumHeight(42)

        self.setIconSize(QSize(22,22))

        if icon is not None:
            self.setIcon(icon)

        self.setStyleSheet("""

QPushButton{

background:#1e293b;

border:1px solid #334155;

border-radius:10px;

color:white;

padding-left:12px;

text-align:left;

font-size:13px;

font-weight:600;

}

QPushButton:hover{

background:#273449;

border:1px solid #00BFFF;

}

QPushButton:pressed{

background:#172033;

}

""")

        apply_shadow(self)


# ==========================================================
# GLASS CARD
# ==========================================================

class GlassCard(BaseCard):

    def __init__(self,title):

        super().__init__()

        self.title = TitleLabel(title)

        self.layout.addWidget(self.title)

        self.layout.addStretch()


# ==========================================================
# STATUS CARD
# ==========================================================

class StatusCard(GlassCard):

    def __init__(self,title):

        super().__init__(title)

        self.value = ValueLabel("Offline")

        self.layout.addWidget(self.value)

    def online(self):

        self.value.setText("ONLINE")

        self.value.setStyleSheet("""

color:#00D26A;

font-size:20px;

font-weight:bold;

""")

    def offline(self):

        self.value.setText("OFFLINE")

        self.value.setStyleSheet("""

color:#FF4C4C;

font-size:20px;

font-weight:bold;

""")


# ==========================================================
# METRIC CARD
# ==========================================================

class MetricCard(GlassCard):

    def __init__(self,title,value="0"):

        super().__init__(title)

        self.metric = ValueLabel(value)

        self.layout.addWidget(self.metric)

    def setMetric(self,value):

        self.metric.setText(str(value))


# ==========================================================
# INFO CARD
# ==========================================================

class InfoCard(GlassCard):

    def __init__(self,title,text=""):

        super().__init__(title)

        self.info = QLabel(text)

        self.info.setWordWrap(True)

        self.info.setStyleSheet("""

color:#B8C7E0;

font-size:12px;

background:transparent;

""")

        self.layout.addWidget(self.info)

    def setText(self,text):

        self.info.setText(str(text))


# ==========================================================
# ANIMATED LABEL
# ==========================================================

class AnimatedLabel(QLabel):

    def __init__(self,text=""):

        super().__init__(text)

        self._opacity = 1.0

        self.animation = QPropertyAnimation(

            self,

            b"opacity"

        )

        self.animation.setDuration(1200)

        self.animation.setStartValue(0.40)

        self.animation.setEndValue(1.00)

        self.animation.setLoopCount(-1)

        self.animation.start()

    def getOpacity(self):

        return self._opacity

    def setOpacity(self,value):

        self._opacity=value

        self.update()

    opacity = Property(

        float,

        getOpacity,

        setOpacity

    )

    def paintEvent(self,event):

        painter=QPainter(self)

        painter.setOpacity(self._opacity)

        painter.setPen(self.palette().windowText().color())

        painter.setFont(self.font())

        painter.drawText(

            self.rect(),

            Qt.AlignCenter,

            self.text()

        )
      # ==========================================================
# CIRCULAR RISK METER
# ==========================================================

class CircularRiskMeter(QWidget):

    def __init__(self, value=0, parent=None):

        super().__init__(parent)

        self._value = value
        self._maximum = 100

        self.setMinimumSize(180, 180)

        self.animation = QPropertyAnimation(
            self,
            b"value"
        )

        self.animation.setDuration(1200)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

    # ----------------------------------------

    def getValue(self):

        return self._value

    def setValue(self, value):

        self._value = max(
            0,
            min(self._maximum, value)
        )

        self.update()

    value = Property(
        int,
        getValue,
        setValue
    )

    # ----------------------------------------

    def animateTo(self, value):

        self.animation.stop()

        self.animation.setStartValue(
            self._value
        )

        self.animation.setEndValue(
            value
        )

        self.animation.start()

    # ----------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        rect = self.rect().adjusted(
            14,
            14,
            -14,
            -14
        )

        # Background Circle

        pen = QPen(
            QColor("#233044"),
            12
        )

        painter.setPen(pen)

        painter.drawEllipse(rect)

        # Progress

        if self._value < 35:

            color = QColor("#00D26A")

        elif self._value < 70:

            color = QColor("#FFB020")

        else:

            color = QColor("#FF4C4C")

        pen = QPen(
            color,
            12
        )

        pen.setCapStyle(
            Qt.RoundCap
        )

        painter.setPen(pen)

        angle = int(
            360 * self._value / self._maximum
        )

        painter.drawArc(
            rect,
            90 * 16,
            -angle * 16
        )

        painter.setPen(
            QColor("white")
        )

        font = QFont(
            "Segoe UI",
            22,
            QFont.Bold
        )

        painter.setFont(font)

        painter.drawText(
            rect,
            Qt.AlignCenter,
            f"{self._value}%"
        )


# ==========================================================
# PROGRESS BAR
# ==========================================================

class ScanProgress(QProgressBar):

    def __init__(self):

        super().__init__()

        self.setRange(
            0,
            100
        )

        self.setValue(0)

        self.setTextVisible(True)

        self.setMinimumHeight(16)

        self.setStyleSheet("""

QProgressBar{

background:#172033;

border-radius:8px;

color:white;

text-align:center;

}

QProgressBar::chunk{

background:#00BFFF;

border-radius:8px;

}

""")


# ==========================================================
# SCAN STATUS
# ==========================================================

class ScanStatusCard(GlassCard):

    def __init__(self):

        super().__init__("Scan Status")

        self.status = AnimatedLabel(
            "Waiting..."
        )

        self.status.setStyleSheet("""

color:#00BFFF;

font-size:15px;

font-weight:bold;

background:transparent;

""")

        self.progress = ScanProgress()

        self.layout.addWidget(
            self.status
        )

        self.layout.addWidget(
            self.progress
        )

    def updateStatus(

        self,

        text,

        value

    ):

        self.status.setText(text)

        self.progress.setValue(value)


# ==========================================================
# LIVE METRIC CARD
# ==========================================================

class LiveMetricCard(GlassCard):

    def __init__(

        self,

        title,

        value="0"

    ):

        super().__init__(title)

        self.metric = ValueLabel(value)

        self.layout.addWidget(

            self.metric

        )

    def updateValue(

        self,

        value

    ):

        self.metric.setText(

            str(value)

        )
      # ==========================================================
# LOADING OVERLAY
# ==========================================================

class LoadingOverlay(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("LoadingOverlay")

        self.setStyleSheet("""

QFrame{

background:rgba(8,15,30,210);

border-radius:12px;

}

""")

        self.setVisible(False)

        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignCenter)

        layout.setSpacing(15)

        self.title = AnimatedLabel("Initializing...")

        self.title.setStyleSheet("""

color:white;

font-size:18px;

font-weight:bold;

background:transparent;

""")

        self.progress = ScanProgress()

        self.progress.setFixedWidth(320)

        self.status = QLabel("Please wait...")

        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("""

color:#B8C7E0;

background:transparent;

font-size:13px;

""")

        layout.addStretch()

        layout.addWidget(self.title)

        layout.addWidget(self.progress)

        layout.addWidget(self.status)

        layout.addStretch()

    def start(self, text="Scanning..."):

        self.title.setText(text)

        self.progress.setValue(0)

        self.status.setText("Starting modules...")

        self.show()

    def update(self, percent, text):

        self.progress.setValue(percent)

        self.status.setText(text)

    def finish(self):

        self.progress.setValue(100)

        self.status.setText("Completed")

        self.hide()


# ==========================================================
# TERMINAL OUTPUT CARD
# ==========================================================

class TerminalCard(GlassCard):

    def __init__(self):

        super().__init__("Terminal Output")

        self.output = QLabel()

        self.output.setWordWrap(True)

        self.output.setAlignment(Qt.AlignTop)

        self.output.setStyleSheet("""

background:#101827;

border:1px solid #263549;

border-radius:8px;

padding:10px;

color:#00FF7F;

font-family:Consolas;

font-size:11px;

""")

        self.output.setMinimumHeight(180)

        self.layout.addWidget(self.output)

    def append(self, text):

        current = self.output.text()

        self.output.setText(

            current +

            text +

            "\n"

        )

    def clear(self):

        self.output.clear()


# ==========================================================
# SCREENSHOT CARD
# ==========================================================

class ScreenshotCard(GlassCard):

    def __init__(self):

        super().__init__("Website Screenshot")

        self.image = QLabel("No Screenshot")

        self.image.setAlignment(Qt.AlignCenter)

        self.image.setMinimumHeight(220)

        self.image.setStyleSheet("""

background:#0F172A;

border:1px solid #334155;

border-radius:10px;

color:#64748B;

""")

        self.layout.addWidget(self.image)

    def setPixmap(self, pixmap):

        if pixmap:

            self.image.setPixmap(

                pixmap.scaled(

                    self.image.size(),

                    Qt.KeepAspectRatio,

                    Qt.SmoothTransformation

                )

            )


# ==========================================================
# AI SUMMARY CARD
# ==========================================================

class AISummaryCard(GlassCard):

    def __init__(self):

        super().__init__("AI Security Summary")

        self.summary = QLabel()

        self.summary.setWordWrap(True)

        self.summary.setAlignment(Qt.AlignTop)

        self.summary.setStyleSheet("""

background:transparent;

color:#E2E8F0;

font-size:12px;

""")

        self.layout.addWidget(self.summary)

    def setSummary(self, text):

        self.summary.setText(text)


# ==========================================================
# EXPORT CARD
# ==========================================================

class ExportCard(GlassCard):

    def __init__(self):

        super().__init__("Reports")

        row = QHBoxLayout()

        self.pdf = GlowButton("Export PDF")

        self.html = GlowButton("Export HTML")

        self.json = GlowButton("Export JSON")

        row.addWidget(self.pdf)

        row.addWidget(self.html)

        row.addWidget(self.json)

        self.layout.addLayout(row)
      # ==========================================================
# DASHBOARD HEADER
# ==========================================================

class DashboardHeader(QWidget):

    def __init__(self, title="CyberScope"):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        self.title = QLabel(title)

        self.title.setStyleSheet("""

color:white;

font-size:26px;

font-weight:bold;

background:transparent;

""")

        self.subtitle = QLabel(

            "Professional Website Intelligence Platform"

        )

        self.subtitle.setStyleSheet("""

color:#94A3B8;

font-size:12px;

background:transparent;

""")

        textLayout = QVBoxLayout()

        textLayout.addWidget(self.title)

        textLayout.addWidget(self.subtitle)

        layout.addLayout(textLayout)

        layout.addStretch()


# ==========================================================
# STATUS INDICATOR
# ==========================================================

class StatusIndicator(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        self.dot = QLabel()

        self.dot.setFixedSize(12,12)

        self.dot.setStyleSheet("""

background:#00D26A;

border-radius:6px;

""")

        self.label = QLabel("READY")

        self.label.setStyleSheet("""

color:white;

font-weight:bold;

""")

        layout.addWidget(self.dot)

        layout.addWidget(self.label)

        layout.addStretch()

    def setStatus(self,text,color="#00D26A"):

        self.label.setText(text)

        self.dot.setStyleSheet(f"""

background:{color};

border-radius:6px;

""")


# ==========================================================
# SEPARATOR
# ==========================================================

class NeonSeparator(QFrame):

    def __init__(self):

        super().__init__()

        self.setFixedHeight(2)

        self.setStyleSheet("""

background:#00BFFF;

border:none;

""")


# ==========================================================
# DASHBOARD ROW
# ==========================================================

class DashboardRow(QWidget):

    def __init__(self,*widgets):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setSpacing(15)

        layout.setContentsMargins(0,0,0,0)

        for widget in widgets:

            layout.addWidget(widget)


# ==========================================================
# SMALL INFO BADGE
# ==========================================================

class InfoBadge(QLabel):

    def __init__(self,text):

        super().__init__(text)

        self.setStyleSheet("""

background:#1E293B;

border:1px solid #00BFFF;

border-radius:12px;

padding:4px 10px;

color:white;

font-size:11px;

""")


# ==========================================================
# FOOTER
# ==========================================================

class DashboardFooter(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        layout.addStretch()

        label = QLabel(

            "CyberScope 2.0  •  by Krunal Paliwal"

        )

        label.setStyleSheet("""

color:#64748B;

font-size:11px;

background:transparent;

""")

        layout.addWidget(label)


# ==========================================================
# COMPONENT EXPORTS
# ==========================================================

__all__ = [

    "GlowButton",
    "IconButton",
    "BaseCard",
    "GlassCard",
    "StatusCard",
    "MetricCard",
    "InfoCard",
    "AnimatedLabel",
    "CircularRiskMeter",
    "ScanProgress",
    "ScanStatusCard",
    "LiveMetricCard",
    "LoadingOverlay",
    "TerminalCard",
    "ScreenshotCard",
    "AISummaryCard",
    "ExportCard",
    "DashboardHeader",
    "StatusIndicator",
    "DashboardRow",
    "DashboardFooter",
    "InfoBadge",
    "NeonSeparator"
]


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication,QVBoxLayout

    import sys

    app = QApplication(sys.argv)

    window = QWidget()

    window.setWindowTitle("CyberScope UI Components")

    window.resize(900,700)

    layout = QVBoxLayout(window)

    layout.setSpacing(20)

    layout.addWidget(DashboardHeader())

    layout.addWidget(StatusIndicator())

    layout.addWidget(NeonSeparator())

    layout.addWidget(

        DashboardRow(

            MetricCard("IP"),

            MetricCard("Ports"),

            MetricCard("Risk")

        )

    )

    layout.addWidget(CircularRiskMeter(73))

    layout.addWidget(ScanStatusCard())

    layout.addWidget(AISummaryCard())

    layout.addWidget(ExportCard())

    layout.addWidget(DashboardFooter())

    window.show()

    sys.exit(app.exec())
