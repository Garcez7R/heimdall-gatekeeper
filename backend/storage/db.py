from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from backend.core.config import load_config


def get_database_path() -> Path:
    config = load_config()
    db_path = config.get("storage", {}).get("sqlite_path", "data/heimdall.db")
    path = Path(db_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[2] / db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(get_database_path())
    connection.row_factory = sqlite3.Row
    try:
      yield connection
      connection.commit()
    finally:
      connection.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'low',
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  raw_payload TEXT,
  ip_address TEXT,
  cve_id TEXT,
  cve_score REAL,
  status TEXT NOT NULL DEFAULT 'new',
  tags TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_name TEXT NOT NULL,
  severity TEXT NOT NULL,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  source TEXT NOT NULL,
  event_id INTEGER,
  ip_address TEXT,
  cve_id TEXT,
  cve_score REAL,
  mitre_tag TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  acknowledged_by TEXT,
  resolved_by TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS rule_hits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_name TEXT NOT NULL,
  total_hits INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cve_cache (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cve_id TEXT NOT NULL UNIQUE,
  score REAL,
  severity TEXT,
  summary TEXT,
  payload TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  metric_key TEXT NOT NULL UNIQUE,
  metric_value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(SCHEMA)


def fetch_all(query: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def fetch_one(query: str, parameters: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(query, parameters).fetchone()
    return dict(row) if row else None


def execute(query: str, parameters: tuple[Any, ...] = ()) -> int:
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return int(cursor.lastrowid or 0)
