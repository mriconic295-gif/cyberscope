"""
=========================================================
CyberScope Workers
Author : Krunal Paliwal
=========================================================
"""

from __future__ import annotations

import traceback

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import Signal
from PyQt5.QtCore import Slot

from modules.scanner import ScannerEngine


# ==========================================================
# Worker Signals
# ==========================================================

class WorkerSignals(QObject):

    started = Signal()

    finished = Signal()

    error = Signal(str)

    progress = Signal(int)

    status = Signal(str)

    result = Signal(dict)

    screenshot = Signal(str)


# ==========================================================
# Base Worker
# ==========================================================

class BaseWorker(QRunnable):

    def __init__(self):

        super().__init__()

        self.signals = WorkerSignals()

        self.setAutoDelete(True)


# ==========================================================
# Scan Worker
# ==========================================================

class ScanWorker(BaseWorker):

    def __init__(self, target):

        super().__init__()

        self.target = target

        self.engine = ScannerEngine()

    @Slot()
    def run(self):

        try:

            self.signals.started.emit()

            self.signals.status.emit(

                "Initializing Scanner..."

            )

            self.signals.progress.emit(5)

            result = self.engine.scan(

                self.target,

                progress_callback=self.signals.progress,

                status_callback=self.signals.status

            )

            self.signals.progress.emit(100)

            self.signals.result.emit(result)

            self.signals.finished.emit()

        except Exception:

            self.signals.error.emit(

                traceback.format_exc()

            )
          # ==========================================================
# Screenshot Worker
# ==========================================================

class ScreenshotWorker(BaseWorker):

    def __init__(self, target):

        super().__init__()

        self.target = target

    @Slot()
    def run(self):

        try:

            from modules.intelligence import ScreenshotEngine

            self.signals.started.emit()

            self.signals.status.emit(

                "Capturing Website Screenshot..."

            )

            engine = ScreenshotEngine()

            image = engine.capture(self.target)

            self.signals.screenshot.emit(image)

            self.signals.finished.emit()

        except Exception:

            self.signals.error.emit(

                traceback.format_exc()

            )


# ==========================================================
# Report Worker
# ==========================================================

class ReportWorker(BaseWorker):

    def __init__(self, data, report_type, output_path):

        super().__init__()

        self.data = data

        self.report_type = report_type.lower()

        self.output_path = output_path

    @Slot()
    def run(self):

        try:

            from reports.report_engine import ReportEngine

            self.signals.started.emit()

            self.signals.status.emit(

                "Generating Report..."

            )

            engine = ReportEngine()

            path = engine.export(

                report_type=self.report_type,

                data=self.data,

                output_path=self.output_path

            )

            self.signals.result.emit({

                "report": path

            })

            self.signals.finished.emit()

        except Exception:

            self.signals.error.emit(

                traceback.format_exc()

            )


# ==========================================================
# Worker Manager
# ==========================================================

class WorkerManager:

    def __init__(self, thread_pool):

        self.thread_pool = thread_pool

    def start_scan(self, worker):

        self.thread_pool.start(worker)

    def start_screenshot(self, worker):

        self.thread_pool.start(worker)

    def start_report(self, worker):

        self.thread_pool.start(worker)
      # ==========================================================
# WORKER CONTROLLER
# ==========================================================

class WorkerController:

    """
    Central Worker Manager

    Responsible for:

    • Scan Worker
    • Screenshot Worker
    • Report Worker

    """

    def __init__(self, thread_pool):

        self.pool = thread_pool

        self.active_workers = []

    # ------------------------------------------------------

    def submit(self, worker):

        self.active_workers.append(worker)

        worker.signals.finished.connect(

            lambda: self.cleanup(worker)

        )

        self.pool.start(worker)

        return worker

    # ------------------------------------------------------

    def cleanup(self, worker):

        if worker in self.active_workers:

            self.active_workers.remove(worker)

    # ------------------------------------------------------

    def running(self):

        return len(self.active_workers)

    # ------------------------------------------------------

    def clear(self):

        self.active_workers.clear()


# ==========================================================
# FACTORY
# ==========================================================

class WorkerFactory:

    @staticmethod
    def scan(target):

        return ScanWorker(target)

    @staticmethod
    def screenshot(target):

        return ScreenshotWorker(target)

    @staticmethod
    def report(

        data,

        report_type,

        output_path

    ):

        return ReportWorker(

            data,

            report_type,

            output_path

        )


# ==========================================================
# VERSION
# ==========================================================

WORKER_NAME = "CyberScope Workers"

WORKER_VERSION = "2.0"


# ==========================================================
# TEST
# ==========================================================

def self_test():

    print("="*50)

    print(WORKER_NAME)

    print(WORKER_VERSION)

    print("="*50)

    print("Workers Ready")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    self_test()
