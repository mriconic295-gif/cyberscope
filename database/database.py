"""
=========================================================
CyberScope Database Engine
Author : Krunal Paliwal
Version : 2.0
=========================================================
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from datetime import datetime


class Database:

    DB_NAME = "history.db"

    def __init__(self, db_path=None):

        if db_path is None:
            db_path = Path(__file__).parent / self.DB_NAME

        self.db_path = str(db_path)

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # -----------------------------------------------------

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS scans(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            target TEXT NOT NULL,

            scan_time TEXT NOT NULL,

            risk_score REAL,

            summary TEXT,

            report_json TEXT

        )

        """)

        self.connection.commit()

    # -----------------------------------------------------

    def save_scan(self, result: dict):

        target = result.get("target", "")

        risk = result.get("risk", 0)

        summary = result.get("summary", "")

        report = json.dumps(result, default=str)

        self.cursor.execute("""

        INSERT INTO scans(

            target,

            scan_time,

            risk_score,

            summary,

            report_json

        )

        VALUES(?,?,?,?,?)

        """, (

            target,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            risk,

            summary,

            report

        ))

        self.connection.commit()

        return self.cursor.lastrowid

    # -----------------------------------------------------

    def history(self):

        self.cursor.execute("""

        SELECT *

        FROM scans

        ORDER BY id DESC

        """)

        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]

    # -----------------------------------------------------

    def get_scan(self, scan_id):

        self.cursor.execute("""

        SELECT *

        FROM scans

        WHERE id=?

        """, (scan_id,))

        row = self.cursor.fetchone()

        if row:

            return dict(row)

        return None

    # -----------------------------------------------------

    def delete_scan(self, scan_id):

        self.cursor.execute("""

        DELETE FROM scans

        WHERE id=?

        """, (scan_id,))

        self.connection.commit()

    # -----------------------------------------------------

    def clear_history(self):

        self.cursor.execute("""

        DELETE FROM scans

        """)

        self.connection.commit()

    # -----------------------------------------------------

    def count(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM scans

        """)

        return self.cursor.fetchone()[0]

    # -----------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()


# ==========================================================
# GLOBAL DATABASE
# ==========================================================

database = Database()


# ==========================================================
# SELF TEST
# ==========================================================

if __name__ == "__main__":

    from database.database import Database

db = Database()

    print("CyberScope Database Ready")

    print(

        "Stored Scans :",

        db.count()

    )

    db.close()
