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

from PyQt5.QtCore import Qt, QTimer
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

    QMessageBox.critical(

        None,

        "CyberScope Error",

        message

    )


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
# WORKER INITIALIZATION
# ============================================================

worker_manager = None


def initialize_workers():

    global worker_manager

    try:

        logger.info("Initializing Workers...")

        worker_manager = WorkerManager()

        if hasattr(worker_manager, "start"):
            worker_manager.start()

        logger.info("Workers Ready")

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

    QApplication.setAttribute(

        Qt.AA_EnableHighDpiScaling,

        True

    )

    QApplication.setAttribute(

        Qt.AA_UseHighDpiPixmaps,

        True

    )

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    app.setApplicationVersion(APP_VERSION)

    app.setOrganizationName(APP_AUTHOR)

    if LOGO.exists():

        app.setWindowIcon(

            QIcon(str(LOGO))

        )

    load_stylesheet(app)

    return app


# ============================================================
# SPLASH SCREEN
# ============================================================

def show_splash():

    splash = SplashScreen()

    splash.show()

    QApplication.processEvents()

    return splash


# ============================================================
# MAIN WINDOW
# ============================================================

def create_main_window():

    window = MainWindow()

    if hasattr(window, "setWindowTitle"):

        window.setWindowTitle(

            f"{APP_NAME} {APP_VERSION}"

        )

    if LOGO.exists():

        window.setWindowIcon(

            QIcon(str(LOGO))

        )

    return window
  # ============================================================
# STARTUP SEQUENCE
# ============================================================

def startup_sequence(splash):

    logger.info("Starting CyberScope...")

    if hasattr(splash, "set_status"):
        splash.set_status("Checking Assets...")

    QApplication.processEvents()

    if not check_resources():
        logger.warning("Some assets are missing.")

    # --------------------------------------------------------

    if hasattr(splash, "set_progress"):
        splash.set_progress(15)

    if hasattr(splash, "set_status"):
        splash.set_status("Initializing Database...")

    QApplication.processEvents()

    if not initialize_database():

        QMessageBox.critical(
            None,
            APP_NAME,
            "Database initialization failed."
        )

        return None

    # --------------------------------------------------------

    if hasattr(splash, "set_progress"):
        splash.set_progress(35)

    if hasattr(splash, "set_status"):
        splash.set_status("Starting Workers...")

    QApplication.processEvents()

    initialize_workers()

    # --------------------------------------------------------

    if hasattr(splash, "set_progress"):
        splash.set_progress(55)

    if hasattr(splash, "set_status"):
        splash.set_status("Loading Interface...")

    QApplication.processEvents()

    window = create_main_window()

    # --------------------------------------------------------

    if hasattr(splash, "set_progress"):
        splash.set_progress(80)

    if hasattr(splash, "set_status"):
        splash.set_status("Preparing Dashboard...")

    QApplication.processEvents()

    if hasattr(window, "initialize"):
        try:
            window.initialize()
        except Exception:
            logger.exception("MainWindow.initialize() failed")

    # --------------------------------------------------------

    if hasattr(splash, "set_progress"):
        splash.set_progress(100)

    if hasattr(splash, "set_status"):
        splash.set_status("Ready")

    QApplication.processEvents()

    return window


# ============================================================
# CLEANUP
# ============================================================

def cleanup():

    logger.info("Cleaning Resources...")

    try:

        global worker_manager

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
# SIGNALS
# ============================================================

def signal_handler(sig, frame):

    logger.info("Exit Signal Received")

    cleanup()

    QApplication.quit()


signal.signal(signal.SIGINT, signal_handler)

try:
    signal.signal(signal.SIGTERM, signal_handler)
except Exception:
    pass


# ============================================================
# SAFE EXIT TIMER
# ============================================================

exit_timer = QTimer()

exit_timer.setInterval(500)

exit_timer.timeout.connect(lambda: None)
# ============================================================
# APPLICATION RUNNER
# ============================================================

def run():

    logger.info("Launching Application")

    app = create_application()

    splash = show_splash()

    window = None

    try:

        window = startup_sequence(splash)

        if window is None:

            logger.error("Startup Failed")

            QMessageBox.critical(

                None,

                APP_NAME,

                "CyberScope failed to initialize."

            )

            return 1

        # -----------------------------

        if hasattr(splash, "finish"):

            splash.finish(window)

        else:

            splash.close()

        # -----------------------------

        window.show()

        logger.info("Main Window Displayed")

        exit_code = app.exec()

        cleanup()

        logger.info("Application Closed")

        return exit_code

    except KeyboardInterrupt:

        logger.warning("Keyboard Interrupt")

        cleanup()

        return 0

    except Exception as e:

        logger.exception(e)

        cleanup()

        QMessageBox.critical(

            None,

            "Fatal Error",

            str(e)

        )

        return 1


# ============================================================
# APPLICATION INFORMATION
# ============================================================

def print_banner():

    banner = f"""

============================================================

              CyberScope

      Professional Website Intelligence Platform

------------------------------------------------------------

Version : {APP_VERSION}

Author  : {APP_AUTHOR}

============================================================

"""

    print(banner)

    logger.info(banner)


# ============================================================
# ENVIRONMENT CHECK
# ============================================================

def check_environment():

    logger.info("Checking Runtime Environment")

    logger.info("Python : %s", sys.version.split()[0])

    logger.info("Qt      : PySide6")

    logger.info("Platform: %s", sys.platform)

    logger.info("Root    : %s", ROOT_DIR)

    if not ROOT_DIR.exists():

        raise RuntimeError(

            "Project Root Missing"

        )

    return True


# ============================================================
# VERIFY REQUIRED DIRECTORIES
# ============================================================

def verify_directories():

    required = [

        ROOT_DIR / "assets",

        ROOT_DIR / "gui",

        ROOT_DIR / "modules",

        ROOT_DIR / "workers",

        ROOT_DIR / "database",

        ROOT_DIR / "themes",

        ROOT_DIR / "utils",

        ROOT_DIR / "reports"

    ]

    for folder in required:

        if not folder.exists():

            logger.warning(

                "Missing Folder : %s",

                folder.name

            )

    logger.info("Directory Verification Finished")
  # ============================================================
# MAIN ENTRY
# ============================================================

def main():

    print_banner()

    try:

        check_environment()

        verify_directories()

    except Exception as error:

        logger.exception(error)

        QMessageBox.critical(

            None,

            APP_NAME,

            f"Startup check failed.\n\n{error}"

        )

        return 1

    try:

        return run()

    except Exception as error:

        logger.exception(error)

        traceback.print_exc()

        return 1

    finally:

        try:

            cleanup()

        except Exception:

            logger.exception(

                "Cleanup failed"

            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    exit_code = 1

    try:

        exit_code = main()

    except KeyboardInterrupt:

        logger.warning(

            "Application Interrupted"

        )

        exit_code = 0

    except Exception as error:

        logger.exception(error)

        traceback.print_exc()

        exit_code = 1

    finally:

        try:

            logging.shutdown()

        except Exception:

            pass

        sys.exit(exit_code)
