"""
===========================================================
 CyberScope
 Professional Website Intelligence Platform

 Author  : Krunal Paliwal
 Version : 2.0
===========================================================
"""

from __future__ import annotations

import os
import sys
import traceback
import logging
import signal

from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
)

# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ============================================================
# IMPORT PROJECT FILES
# ============================================================

try:
    from gui.main_window import MainWindow
    from gui.splash_screen import SplashScreen

    from database.database import Database
    from workers.workers import WorkerManager
    from utils.logger import setup_logger
    from version import __version__

except Exception as error:
    print("\nIMPORT ERROR\n")
    print(error)
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# APPLICATION INFO
# ============================================================

APP_NAME = "CyberScope"
APP_VERSION = __version__
APP_AUTHOR = "Krunal Paliwal"

# ============================================================
# ASSETS
# ============================================================

ASSETS = ROOT_DIR / "assets"
LOGO = ASSETS / "logo.png"
SPLASH = ASSETS / "splash.png"
BACKGROUND = ASSETS / "background.png"
LOADING = ASSETS / "loading.gif"

# ============================================================
# LOGGING
# ============================================================

logger = setup_logger()

logger.info("=" * 60)
logger.info("CyberScope Starting...")
logger.info("Version : %s", APP_VERSION)
logger.info("=" * 60)

# ============================================================
# GLOBAL EXCEPTION
# ============================================================

def exception_handler(exc_type, exc_value, exc_traceback):
    message = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )
    logger.critical(message)
    
    if QApplication.instance():
        QMessageBox.critical(
            None,
            "CyberScope Error",
            message
        )
    else:
        print(f"CRITICAL ERROR: {message}")

sys.excepthook = exception_handler

# ============================================================
# RESOURCE CHECK
# ============================================================

def check_resources():
    required = [
        LOGO,
        SPLASH,
        BACKGROUND,
        LOADING,
    ]

    missing = []
    for item in required:
        if not item.exists():
            missing.append(item.name)

    if missing:
        logger.warning(
            "Missing Assets : %s",
            ", ".join(missing)
        )
        return False
    return True

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

database = None

def initialize_database():
    global database
    try:
        logger.info("Initializing Database...")
        database = Database()

        if hasattr(database, "connect"):
            database.connect()
        elif hasattr(database, "initialize"):
            database.initialize()

        logger.info("Database Ready")
        return True

    except Exception as e:
        logger.exception(e)
        return False

# ============================================================
# WORKER INITIALIZATION (FIXED SCAN THREAD POOL)
# ============================================================

worker_manager = None
thread_pool = None

def initialize_workers():
    global worker_manager, thread_pool
    try:
        logger.info("Initializing Workers...")
        
        # Dedicated Thread Pool for Multi-threading scan tasks
        thread_pool = QThreadPool.globalInstance()
        thread_pool.setMaxThreadCount(20)
        
        worker_manager = WorkerManager(thread_pool)

        if hasattr(worker_manager, "start"):
            worker_manager.start()

        logger.info("Workers Ready with Active ThreadPool")
        return True

    except Exception as e:
        logger.exception(e)
        return False

# ============================================================
# LOAD STYLESHEET
# ============================================================

STYLE_FILE = ROOT_DIR / "themes" / "style.qss"

def load_stylesheet(app):
    if not STYLE_FILE.exists():
        logger.warning("style.qss not found")
        return

    try:
        with open(
            STYLE_FILE,
            "r",
            encoding="utf-8"
        ) as style:
            app.setStyleSheet(style.read())
            logger.info("Theme Loaded")

    except Exception as e:
        logger.exception(e)

# ============================================================
# APPLICATION
# ============================================================

def create_application():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_AUTHOR)

    if LOGO.exists():
        app.setWindowIcon(QIcon(str(LOGO)))

    load_stylesheet(app)
    return app

# ============================================================
# SPLASH SCREEN
# ============================================================

def show_splash():
    try:
        splash = SplashScreen()
        splash.show()
        QApplication.processEvents()
        return splash
    except Exception as e:
        logger.warning(f"Splash screen bypassed: {e}")
        return None

# ============================================================
# MAIN WINDOW
# ============================================================

def create_main_window():
    window = MainWindow()

    if hasattr(window, "setWindowTitle"):
        window.setWindowTitle(f"{APP_NAME} {APP_VERSION}")

    if LOGO.exists():
        window.setWindowIcon(QIcon(str(LOGO)))

    # Global worker reference attached to MainWindow for scanning
    window.worker_manager = worker_manager
    window.thread_pool = thread_pool

    return window

# ============================================================
# STARTUP SEQUENCE
# ============================================================

def startup_sequence(splash):
    logger.info("Starting CyberScope Sequence...")

    if splash and hasattr(splash, "set_status"):
        splash.set_status("Checking Assets...")
    QApplication.processEvents()

    check_resources()

    # --------------------------------------------------------
    if splash and hasattr(splash, "set_progress"):
        splash.set_progress(20)
    if splash and hasattr(splash, "set_status"):
        splash.set_status("Initializing Database...")
    QApplication.processEvents()

    if not initialize_database():
        logger.error("Database Init Failed")

    # --------------------------------------------------------
    if splash and hasattr(splash, "set_progress"):
        splash.set_progress(50)
    if splash and hasattr(splash, "set_status"):
        splash.set_status("Starting Workers...")
    QApplication.processEvents()
    
    initialize_workers()

    # --------------------------------------------------------
    if splash and hasattr(splash, "set_progress"):
        splash.set_progress(80)
    if splash and hasattr(splash, "set_status"):
        splash.set_status("Loading Interface...")
    QApplication.processEvents()
    
    window = create_main_window()

    if hasattr(window, "initialize"):
        try:
            window.initialize()
        except Exception:
            logger.exception("MainWindow.initialize() failed")

    if splash and hasattr(splash, "set_progress"):
        splash.set_progress(100)
    QApplication.processEvents()
    
    return window

# ============================================================
# CLEANUP
# ============================================================

def cleanup():
    logger.info("Cleaning Resources...")

    try:
        global worker_manager, thread_pool
        if thread_pool:
            thread_pool.clear()
            thread_pool.waitForDone(1000)
            
        if worker_manager:
            if hasattr(worker_manager, "stop"):
                worker_manager.stop()
            elif hasattr(worker_manager, "shutdown"):
                worker_manager.shutdown()
    except Exception:
        logger.exception("Worker cleanup failed")

    try:
        global database
        if database:
            if hasattr(database, "close"):
                database.close()
            elif hasattr(database, "disconnect"):
                database.disconnect()
    except Exception:
        logger.exception("Database cleanup failed")

    logger.info("Shutdown Complete")

# ============================================================
# SIGNALS & RUNNER
# ============================================================

def signal_handler(sig, frame):
    cleanup()
    QApplication.quit()

signal.signal(signal.SIGINT, signal_handler)

try:
    signal.signal(signal.SIGTERM, signal_handler)
except Exception:
    pass

exit_timer = QTimer()
exit_timer.setInterval(500)
exit_timer.timeout.connect(lambda: None)

def run():
    logger.info("Launching Application")

    app = create_application()
    exit_timer.start()

    splash = show_splash()
    window = startup_sequence(splash)

    if window is None:
        logger.error("Startup Failed")
        return 1

    # FIXED: Handled Single Window Displaying properly
    if splash and hasattr(splash, "finish"):
        splash.finish(window)
    else:
        if splash:
            splash.close()
        window.show()

    logger.info("Main Window Displayed")

    exit_code = app.exec_()
    cleanup()
    return exit_code

# ============================================================
# ENTRY POINT
# ============================================================

def main():
    try:
        return run()
    except Exception as error:
        logger.exception(error)
        traceback.print_exc()
        return 1
    finally:
        cleanup()

if __name__ == "__main__":
    sys.exit(main())
