import json
import sqlite3
from datetime import datetime

DB_NAME = "runs.db"


def init_db():
  with sqlite3.connect(DB_NAME) as conn:
    conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                summary TEXT,
                tests TEXT
            )
        """)
    conn.commit()


def save_run(run_data):
  init_db()
  with sqlite3.connect(DB_NAME) as conn:
    conn.execute(
        "INSERT INTO runs (timestamp, summary, tests) VALUES (?, ?, ?)",
        (
            run_data["timestamp"],
            json.dumps(run_data["summary"]),
            json.dumps(run_data["tests"]),
        ),
    )
    conn.commit()


def get_all_runs():
  init_db()
  with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, summary, tests FROM runs ORDER BY id DESC")
    rows = cursor.fetchall()

    runs = []
    for row in rows:
      runs.append({
          "timestamp": row[0],
          "summary": json.loads(row[1]),
          "tests": json.loads(row[2]),
      })
    return runs
