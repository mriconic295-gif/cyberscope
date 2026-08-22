"""
=========================================================
CyberScope
Main Application Window

Author : Krunal Paliwal
=========================================================
"""

import sys
from pathlib import Path

from PyQt5.QtCore import (
    Qt,
    QSize,
    pyqtSignal
)

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QStackedWidget,
    QMessageBox,
    QSizePolicy,
    QFrame,
    QStatusBar,
    QApplication,
    QAction
)

# ----------------------------------------------------
# Internal Imports
# ----------------------------------------------------

from gui.sidebar import Sidebar
from gui.title_bar import TitleBar
from gui.dashboard import Dashboard

from themes.dark_theme import theme

from config.constants import *

from version import *


class MainWindow(QMainWindow):

    scanRequested = pyqtSignal(str)

    # ==================================================

    def __init__(self):

        super().__init__()

        self.setObjectName("MainWindow")

        self.setWindowTitle(WINDOW_TITLE)

        # Optimization for Low-End PC Displays
        self.setMinimumSize(1024, 600)

        if Path(APP_ICON).exists():
            self.setWindowIcon(
                QIcon(str(APP_ICON))
            )

        # Frameless Window
        self.setWindowFlags(
            Qt.FramelessWindowHint
        )

        # Main Widget
        self.central = QWidget()

        self.setCentralWidget(self.central)

        # Layout
        self.mainLayout = QHBoxLayout(self.central)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.setSpacing(0)

        # Apply Theme
        app_inst = self.application_instance()
        if app_inst:
            theme.apply(app_inst)

        # Workers placeholder
        self.worker_manager = None
        self.thread_pool = None

        # UI
        self.build_ui()

        self.connect_signals()

        self.create_statusbar()

    # ==================================================

    def application_instance(self):

        return QApplication.instance()

    # ==================================================

    def build_ui(self):

        # --------------------------------------
        # Sidebar
        # --------------------------------------

        self.sidebar = Sidebar()

        self.mainLayout.addWidget(
            self.sidebar
        )

        # --------------------------------------
        # Right Container
        # --------------------------------------

        self.rightContainer = QWidget()

        self.rightLayout = QVBoxLayout(
            self.rightContainer
        )

        self.rightLayout.setContentsMargins(
            0, 0, 0, 0
        )

        self.rightLayout.setSpacing(0)

        self.mainLayout.addWidget(
            self.rightContainer
        )

        # --------------------------------------
        # Title Bar
        # --------------------------------------

        self.titleBar = TitleBar(self)

        self.rightLayout.addWidget(
            self.titleBar
        )

        # --------------------------------------
        # Toolbar
        # --------------------------------------

        self.build_toolbar()

        # --------------------------------------
        # Central Pages
        # --------------------------------------

        self.stack = QStackedWidget()

        self.rightLayout.addWidget(
            self.stack
        )

        # Dashboard
        self.dashboard = Dashboard()

        self.stack.addWidget(
            self.dashboard
        )

    # ==================================================

    def build_toolbar(self):

        self.toolbarWidget = QWidget()

        self.toolbarWidget.setObjectName(
            "topBar"
        )

        layout = QHBoxLayout(
            self.toolbarWidget
        )

        layout.setContentsMargins(
            15, 12, 15, 12
        )

        layout.setSpacing(12)

        # Search
        self.targetInput = QLineEdit()

        self.targetInput.setPlaceholderText(
            "Enter Domain / Website"
        )

        self.targetInput.setMinimumHeight(42)

        # Analyze
        self.analyzeButton = QPushButton(
            "Analyze"
        )

        self.analyzeButton.setMinimumHeight(42)

        # Import
        self.importButton = QPushButton(
            "Import"
        )

        self.importButton.setObjectName(
            "importButton"
        )

        self.importButton.setMinimumHeight(42)

        # Export
        self.exportButton = QPushButton(
            "Export"
        )

        self.exportButton.setObjectName(
            "exportButton"
        )

        self.exportButton.setMinimumHeight(42)

        layout.addWidget(
            self.targetInput,
            1
        )

        layout.addWidget(
            self.analyzeButton
        )

        layout.addWidget(
            self.importButton
        )

        layout.addWidget(
            self.exportButton
        )

        self.rightLayout.addWidget(
            self.toolbarWidget
        )

    # ==================================================
    # Connect Signals
    # ==================================================

    def connect_signals(self):

        # -----------------------------
        # Sidebar
        # -----------------------------

        if hasattr(self.sidebar, 'pageChanged'):
            self.sidebar.pageChanged.connect(
                self.change_page
            )

        # -----------------------------
        # Title Bar
        # -----------------------------

        if hasattr(self.titleBar, 'minimizeRequested'):
            self.titleBar.minimizeRequested.connect(
                self.showMinimized
            )

        if hasattr(self.titleBar, 'maximizeRequested'):
            self.titleBar.maximizeRequested.connect(
                self.toggle_maximize
            )

        if hasattr(self.titleBar, 'closeRequested'):
            self.titleBar.closeRequested.connect(
                self.close
            )

        # -----------------------------
        # Toolbar
        # -----------------------------

        self.analyzeButton.clicked.connect(
            self.start_scan
        )

        self.importButton.clicked.connect(
            self.import_domains
        )

        self.exportButton.clicked.connect(
            self.export_report
        )

        self.targetInput.returnPressed.connect(
            self.start_scan
        )

    # ==================================================
    # Status Bar
    # ==================================================

    def create_statusbar(self):

        self.status = QStatusBar()

        self.status.showMessage(
            "CyberScope Ready"
        )

        self.setStatusBar(
            self.status
        )

    # ==================================================
    # Change Page
    # ==================================================

    def change_page(self, page):

        self.status.showMessage(
            f"Opening : {page}"
        )

        if isinstance(page, int):
            if 0 <= page < self.stack.count():
                self.stack.setCurrentIndex(page)
        elif isinstance(page, str):
            for i in range(self.stack.count()):
                widget = self.stack.widget(i)
                if hasattr(widget, 'objectName') and widget.objectName().lower() == page.lower():
                    self.stack.setCurrentIndex(i)
                    break

    # ==================================================
    # Start Scan
    # ==================================================

    def start_scan(self):

        target = self.targetInput.text().strip()

        if not target:

            QMessageBox.warning(
                self,
                "CyberScope",
                "Please enter a domain."
            )

            return

        self.status.showMessage(
            f"Scanning {target}..."
        )

        self.scanRequested.emit(
            target
        )

        # Direct Background Thread Execution
        if hasattr(self, 'dashboard') and hasattr(self.dashboard, 'start_async_scan'):
            self.dashboard.start_async_scan(target)

    # ==================================================
    # Import Domains
    # ==================================================

    def import_domains(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Domains",
            "",
            "Text Files (*.txt)"
        )

        if not filename:
            return

        self.status.showMessage(
            f"Imported : {Path(filename).name}"
        )

    # ==================================================
    # Export
    # ==================================================

    def export_report(self):

        QMessageBox.information(
            self,
            "CyberScope",
            "Report Export Module Coming Soon."
        )

    # ==================================================
    # Maximize / Restore
    # ==================================================

    def toggle_maximize(self):

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # ==================================================
    # Drag Window
    # ==================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos()

        super().mousePressEvent(event)

    # ==================================================
    # Move Window
    # ==================================================

    def mouseMoveEvent(self, event):

        if self.isMaximized():
            return

        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            delta = event.globalPos() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPos()

        super().mouseMoveEvent(event)

    # ==================================================
    # Keyboard Shortcut
    # ==================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_F5:
            self.start_scan()

        elif event.key() == Qt.Key_F11:
            self.toggle_maximize()

        elif event.key() == Qt.Key_Escape:
            if self.isMaximized():
                self.showNormal()

        super().keyPressEvent(event)

    # ==================================================
    # Theme Reload
    # ==================================================

    def reload_theme(self):

        try:
            app_inst = self.application_instance()
            if app_inst:
                theme.apply(app_inst)

            self.status.showMessage(
                "Theme Reloaded"
            )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Theme",
                str(error)
            )

    # ==================================================
    # Scan Finished
    # ==================================================

    def scan_finished(self):

        self.status.showMessage(
            "Recon Completed"
        )

    # ==================================================
    # Scan Error
    # ==================================================

    def scan_error(self, message):

        QMessageBox.critical(
            self,
            "Scan Error",
            message
        )

    # ==================================================
    # Dashboard Refresh
    # ==================================================

    def refresh_dashboard(self):

        try:
            if hasattr(self.dashboard, 'refresh'):
                self.dashboard.refresh()
        except Exception:
            pass

    # ==================================================
    # Resize Event
    # ==================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

    # ==================================================
    # Close Event
    # ==================================================

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self,
            "Exit",
            "Do you really want to exit CyberScope?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # ==================================================
    # Load Modules
    # ==================================================

    def load_modules(self):

        pass

    # ==================================================
    # Initialize Workers
    # ==================================================

    def initialize_workers(self):

        pass

    # ==================================================
    # AI Summary
    # ==================================================

    def show_ai_summary(self, summary):

        try:
            if hasattr(self.dashboard, 'ai_summary'):
                self.dashboard.ai_summary.setPlainText(
                    summary
                )
        except Exception:
            pass

    # ==================================================
    # Risk Score
    # ==================================================

    def update_risk_score(self, score):

        try:
            if hasattr(self.dashboard, 'update_score'):
                self.dashboard.update_score(
                    score
                )
        except Exception:
            pass

    # ==================================================
    # Register Scan Modules
    # ==================================================

    def register_modules(self):

        self.modules = {}

    # ==================================================
    # Start Worker
    # ==================================================

    def start_worker(self, worker):

        try:
            if hasattr(worker, 'finished'):
                worker.finished.connect(self.scan_finished)
            if hasattr(worker, 'error'):
                worker.error.connect(self.scan_error)
            if hasattr(worker, 'progress'):
                worker.progress.connect(self.update_progress)
            
            if hasattr(worker, 'start'):
                worker.start()

        except Exception as error:
            self.scan_error(str(error))

    # ==================================================
    # Progress Update
    # ==================================================

    def update_progress(self, value):

        try:
            self.status.showMessage(
                f"Scanning... {value}%"
            )
        except Exception:
            pass

    # ==================================================
    # Save Window State
    # ==================================================

    def save_window_state(self):

        pass

    # ==================================================
    # Restore Window State
    # ==================================================

    def restore_window_state(self):

        pass

    # ==================================================
    # Load User Settings
    # ==================================================

    def load_settings(self):

        pass

    # ==================================================
    # Cleanup Resources
    # ==================================================

    def cleanup(self):

        pass

    # ==================================================
    # Application Exit
    # ==================================================

    def shutdown(self):

        self.cleanup()
        self.save_window_state()
        self.close()

    # ==================================================
    # About CyberScope
    # ==================================================

    def about(self):

        QMessageBox.about(
            self,
            "CyberScope",
            f"""
<b>{APP_NAME}</b><br>
Version : {APP_VERSION}<br>
Author : Krunal Paliwal<br><br>
Professional Website Reconnaissance Toolkit<br>
Powered by Python + Qt
            """
        )

    # ==================================================
    # Window Loaded
    # ==================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.status.showMessage(
            "CyberScope Ready"
        )

    # ==================================================
    # Window Hidden
    # ==================================================

    def hideEvent(self, event):

        super().hideEvent(event)

    # ==================================================
    # Focus
    # ==================================================

    def focusInEvent(self, event):

        super().focusInEvent(event)

    # ==================================================
    # Focus Lost
    # ==================================================

    def focusOutEvent(self, event):

        super().focusOutEvent(event)
