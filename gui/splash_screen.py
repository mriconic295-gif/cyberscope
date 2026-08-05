"""
=========================================================
CyberScope
Professional Splash Screen

Author : Krunal Paliwal
=========================================================
"""

from pathlib import Path

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve
)

from PyQt5.QtGui import (
    QColor,
    QFont,
    QPixmap,
    QMovie
)

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QGraphicsOpacityEffect
)

from version import (
    SPLASH_TITLE,
    SPLASH_AUTHOR
)

from config.constants import (
    SPLASH,
    LOADING
)


class SplashScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        # Adjusted for low-resolution displays & specs
        self.setFixedSize(700, 420)

        self.setObjectName("SplashScreen")

        self.build_ui()

        self.fade_animation()

        self.start_loading()

    # =====================================================

    def build_ui(self):

        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.setContentsMargins(30, 30, 30, 20)

        self.mainLayout.setSpacing(10)

        self.mainLayout.setAlignment(Qt.AlignCenter)

        # ---------------------------------------
        # Logo
        # ---------------------------------------

        self.logo = QLabel()

        if Path(SPLASH).exists():

            pix = QPixmap(str(SPLASH))

            self.logo.setPixmap(
                pix.scaled(
                    120,
                    120,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        self.logo.setAlignment(Qt.AlignCenter)

        # ---------------------------------------
        # Title
        # ---------------------------------------

        self.title = QLabel(SPLASH_TITLE)

        self.title.setAlignment(Qt.AlignCenter)

        self.title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        self.title.setStyleSheet("""
            color: #00FF88;
        """)

        # ---------------------------------------
        # Subtitle
        # ---------------------------------------

        self.subtitle = QLabel(
            "AI BASED WAPT & OSINT ANALYZER"
        )

        self.subtitle.setAlignment(Qt.AlignCenter)

        self.subtitle.setStyleSheet("""
            color: #A8B3BF;
            font-size: 12px;
        """)

        # ---------------------------------------
        # Loading GIF / Animation
        # ---------------------------------------

        self.loadingLabel = QLabel()

        self.loadingLabel.setAlignment(Qt.AlignCenter)

        if Path(LOADING).exists():

            movie = QMovie(str(LOADING))

            self.loadingLabel.setMovie(movie)

            movie.start()

        # ---------------------------------------
        # Progress Bar
        # ---------------------------------------

        self.progress = QProgressBar()

        self.progress.setMinimum(0)

        self.progress.setMaximum(100)

        self.progress.setValue(0)

        self.progress.setTextVisible(False)

        self.progress.setFixedHeight(6)

        # ---------------------------------------
        # Status
        # ---------------------------------------

        self.status = QLabel(
            "Initializing CyberScope..."
        )

        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("""
            color: white;
            font-size: 11px;
        """)

        # ---------------------------------------
        # Footer
        # ---------------------------------------

        footerLayout = QHBoxLayout()

        footerLayout.addStretch()

        self.author = QLabel(SPLASH_AUTHOR)

        self.author.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Bold
            )
        )

        self.author.setStyleSheet("""
            color: #00FF88;
        """)

        footerLayout.addWidget(self.author)

        # ---------------------------------------
        # Add Widgets
        # ---------------------------------------

        self.mainLayout.addStretch()

        self.mainLayout.addWidget(self.logo)

        self.mainLayout.addWidget(self.title)

        self.mainLayout.addWidget(self.subtitle)

        self.mainLayout.addSpacing(10)

        self.mainLayout.addWidget(self.loadingLabel)

        self.mainLayout.addSpacing(10)

        self.mainLayout.addWidget(self.progress)

        self.mainLayout.addWidget(self.status)

        self.mainLayout.addStretch()

        self.mainLayout.addLayout(footerLayout)

    # =====================================================

    def fade_animation(self):

        effect = QGraphicsOpacityEffect(self)

        self.setGraphicsEffect(effect)

        self.animation = QPropertyAnimation(
            effect,
            b"opacity"
        )

        self.animation.setDuration(600)  # Faster transition for low spec

        self.animation.setStartValue(0)

        self.animation.setEndValue(1)

        self.animation.setEasingCurve(
            QEasingCurve.OutQuad
        )

        self.animation.start()

    # =====================================================

    def start_loading(self):

        self.value = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_progress
        )

        self.timer.start(30)

    # =====================================================

    def update_progress(self):

        self.value += 1

        self.progress.setValue(self.value)

        if self.value < 10:
            self.status.setText("Loading CyberScope Core...")

        elif self.value < 20:
            self.status.setText("Initializing GUI Engine...")

        elif self.value < 30:
            self.status.setText("Loading Theme Manager...")

        elif self.value < 40:
            self.status.setText("Preparing Dashboard...")

        elif self.value < 50:
            self.status.setText("Loading Recon Modules...")

        elif self.value < 60:
            self.status.setText("Initializing DNS Analyzer...")

        elif self.value < 70:
            self.status.setText("Loading Security Engine...")

        elif self.value < 80:
            self.status.setText("Preparing AI Engine...")

        elif self.value < 90:
            self.status.setText("Building Workspace...")

        elif self.value < 100:
            self.status.setText("Finalizing...")

        else:
            self.timer.stop()
            self.finish_loading()

    # =====================================================

    def finish_loading(self):

        self.status.setText("CyberScope Ready")

        self.fade_out()

    # =====================================================

    def fade_out(self):

        self.opacity = QGraphicsOpacityEffect(self)

        self.setGraphicsEffect(self.opacity)

        self.fade = QPropertyAnimation(
            self.opacity,
            b"opacity"
        )

        self.fade.setDuration(400)

        self.fade.setStartValue(1)

        self.fade.setEndValue(0)

        self.fade.setEasingCurve(
            QEasingCurve.InQuad
        )

        self.fade.finished.connect(
            self.launch_main_window
        )

        self.fade.start()

    # =====================================================

    def launch_main_window(self):

        try:
            from gui.main_window import MainWindow

            self.main_window = MainWindow()

            self.main_window.show()

        except Exception as error:

            print("Main Window Error:", error)

        self.close()

    # =====================================================

    @staticmethod
    def start():

        splash = SplashScreen()

        splash.show()

        return splash
