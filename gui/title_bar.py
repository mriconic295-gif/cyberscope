"""
=========================================================
CyberScope
Custom Title Bar
Author : Krunal Paliwal
=========================================================
"""

from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout
)

from version import WINDOW_TITLE
from config.constants import APP_ICON


class TitleBar(QWidget):

    minimizeRequested = Signal()

    maximizeRequested = Signal()

    closeRequested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parentWindow = parent

        self.dragPos = QPoint()

        self.setObjectName("TitleBar")

        self.setFixedHeight(48)

        self.build_ui()

    # ==================================================

    def build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(15, 0, 10, 0)

        layout.setSpacing(8)

        # -----------------------------
        # App Icon
        # -----------------------------

        self.icon = QLabel()

        self.icon.setFixedSize(26, 26)

        self.icon.setPixmap(
            QIcon(str(APP_ICON)).pixmap(22, 22)
        )

        # -----------------------------
        # Title
        # -----------------------------

        self.title = QLabel(WINDOW_TITLE)

        self.title.setObjectName("titleLabel")

        # -----------------------------
        # Spacer
        # -----------------------------

        layout.addWidget(self.icon)

        layout.addWidget(self.title)

        layout.addStretch()

        # -----------------------------
        # Minimize
        # -----------------------------

        self.minBtn = QPushButton("—")

        self.minBtn.setFixedSize(38, 30)

        self.minBtn.clicked.connect(
            self.minimizeRequested.emit
        )

        # -----------------------------
        # Maximize
        # -----------------------------

        self.maxBtn = QPushButton("□")

        self.maxBtn.setFixedSize(38, 30)

        self.maxBtn.clicked.connect(
            self.maximizeRequested.emit
        )

        # -----------------------------
        # Close
        # -----------------------------

        self.closeBtn = QPushButton("✕")

        self.closeBtn.setFixedSize(38, 30)

        self.closeBtn.clicked.connect(
            self.closeRequested.emit
        )

        layout.addWidget(self.minBtn)

        layout.addWidget(self.maxBtn)

        layout.addWidget(self.closeBtn)

    # ==================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragPos = event.globalPosition().toPoint()

    # ==================================================

    def mouseMoveEvent(self, event):

        if not self.parentWindow:

            return

        if event.buttons() == Qt.LeftButton:

            delta = (
                event.globalPosition().toPoint()
                - self.dragPos
            )

            self.parentWindow.move(
                self.parentWindow.pos() + delta
            )

            self.dragPos = event.globalPosition().toPoint()
                # ==================================================
    # Double Click = Maximize / Restore
    # ==================================================

    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.maximizeRequested.emit()

    # ==================================================
    # Update Title
    # ==================================================

    def set_title(self, text):

        self.title.setText(text)

    # ==================================================
    # Set Icon
    # ==================================================

    def set_icon(self, icon_path):

        try:

            icon = QIcon(str(icon_path))

            self.icon.setPixmap(
                icon.pixmap(22, 22)
            )

        except Exception:

            pass
