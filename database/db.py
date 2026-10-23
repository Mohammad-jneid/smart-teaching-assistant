"""SQLite storage for students, attendance and unmatched faces."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from config import settings
from config.constants import STATUS_PRESENT

_SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code  TEXT NOT NULL UNIQUE COLLATE NOCASE,
    full_name     TEXT NOT NULL,
    grade         TEXT NOT NULL DEFAULT '',
    phone         TEXT NOT NULL DEFAULT '',
    notes         TEXT NOT NULL DEFAULT '',
    face_path     TEXT,
    face_encoding TEXT,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER,
    student_code    TEXT NOT NULL,
    full_name       TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'Present',
    distance        REAL,
    similarity      REAL,
    taken_at        TEXT NOT NULL,
    attendance_date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS unregistered (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    face_path     TEXT,
    face_encoding TEXT,
    distance      REAL,
    note          TEXT NOT NULL DEFAULT '',
    seen_at       TEXT NOT NULL,
    seen_date     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance (attendance_date);
CREATE INDEX IF NOT EXISTS idx_unregistered_date ON unregistered (seen_date);
"""


def _now_parts() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d")


def _resolve_db_path(db_path: str | Path | None = None) -> Path:
    path = Path(db_path) if db_path is not None else Path(settings.DB_PATH)
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def get_connection(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(_resolve_db_path(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db(db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.executescript(_SCHEMA)


def _as_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _encoding_blob(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(list(value))


def add_student(
    student_code: str,
    full_name: str,
    grade: str = "",
    phone: str = "",
    notes: str = "",
    face_path: str | None = None,
    face_encoding: Any = None,
    db_path: str | Path | None = None,
) -> int:
    created_at, _ = _now_parts()
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO students
                (student_code, full_name, grade, phone, notes, face_path, face_encoding, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_code.strip(),
                full_name.strip(),
                grade.strip(),
                phone.strip(),
                notes.strip(),
                face_path,
                _encoding_blob(face_encoding),
                created_at,
            ),
        )
        return int(cursor.lastrowid)


def student_code_exists(student_code: str, db_path: str | Path | None = None) -> bool:
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT 1 FROM students WHERE student_code = ? LIMIT 1",
            (student_code.strip(),),
        ).fetchone()
    return row is not None


def get_students(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY full_name COLLATE NOCASE"
        ).fetchall()
    return [dict(row) for row in rows]


def get_students_with_encodings(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM students WHERE face_encoding IS NOT NULL"
        ).fetchall()
    return [dict(row) for row in rows]


def get_student(student_id: int, db_path: str | Path | None = None) -> dict[str, Any] | None:
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()
    return _as_dict(row)


def delete_student(student_id: int, db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.execute("DELETE FROM students WHERE id = ?", (student_id,))


def add_attendance(
    student_id: int | None,
    student_code: str,
    full_name: str,
    status: str = STATUS_PRESENT,
    distance: float | None = None,
    similarity: float | None = None,
    db_path: str | Path | None = None,
) -> int:
    taken_at, attendance_date = _now_parts()
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO attendance
                (student_id, student_code, full_name, status, distance, similarity,
                 taken_at, attendance_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                student_code,
                full_name,
                status,
                distance,
                similarity,
                taken_at,
                attendance_date,
            ),
        )
        return int(cursor.lastrowid)


def has_attendance_today(student_id: int, db_path: str | Path | None = None) -> bool:
    _, attendance_date = _now_parts()
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT 1 FROM attendance WHERE student_id = ? AND attendance_date = ? LIMIT 1",
            (student_id, attendance_date),
        ).fetchone()
    return row is not None


def get_attendance(
    limit: int = 500,
    date: str | None = None,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    query = "SELECT * FROM attendance"
    params: list[Any] = []
    if date:
        query += " WHERE attendance_date = ?"
        params.append(date)
    query += " ORDER BY taken_at DESC, id DESC LIMIT ?"
    params.append(int(limit))

    with get_connection(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def clear_attendance(db_path: str | Path | None = None) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.execute("DELETE FROM attendance")
        return int(cursor.rowcount)


def add_unregistered(
    face_path: str | None,
    distance: float | None = None,
    note: str = "",
    face_encoding: Any = None,
    db_path: str | Path | None = None,
) -> int:
    seen_at, seen_date = _now_parts()
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO unregistered
                (face_path, face_encoding, distance, note, seen_at, seen_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                face_path,
                _encoding_blob(face_encoding),
                distance,
                note,
                seen_at,
                seen_date,
            ),
        )
        return int(cursor.lastrowid)


def get_unregistered(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT * FROM unregistered ORDER BY seen_at DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_unregistered_entry(
    entry_id: int, db_path: str | Path | None = None
) -> dict[str, Any] | None:
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM unregistered WHERE id = ?",
            (entry_id,),
        ).fetchone()
    return _as_dict(row)


def delete_unregistered(entry_id: int, db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.execute("DELETE FROM unregistered WHERE id = ?", (entry_id,))


def clear_unregistered(db_path: str | Path | None = None) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.execute("DELETE FROM unregistered")
        return int(cursor.rowcount)


def promote_unregistered(
    entry_id: int,
    student_code: str,
    full_name: str,
    grade: str = "",
    phone: str = "",
    notes: str = "",
    db_path: str | Path | None = None,
) -> int:
    created_at, _ = _now_parts()
    with get_connection(db_path) as connection:
        entry = connection.execute(
            "SELECT * FROM unregistered WHERE id = ?",
            (entry_id,),
        ).fetchone()
        if entry is None:
            raise ValueError("That unmatched face no longer exists.")

        duplicate = connection.execute(
            "SELECT 1 FROM students WHERE student_code = ? LIMIT 1",
            (student_code.strip(),),
        ).fetchone()
        if duplicate is not None:
            raise ValueError("That student code is already registered.")

        cursor = connection.execute(
            """
            INSERT INTO students
                (student_code, full_name, grade, phone, notes, face_path, face_encoding, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_code.strip(),
                full_name.strip(),
                grade.strip(),
                phone.strip(),
                notes.strip(),
                entry["face_path"],
                entry["face_encoding"],
                created_at,
            ),
        )
        connection.execute("DELETE FROM unregistered WHERE id = ?", (entry_id,))
        return int(cursor.lastrowid)


def get_stats(db_path: str | Path | None = None) -> dict[str, int]:
    _, attendance_date = _now_parts()
    with get_connection(db_path) as connection:
        students = connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        attendance_today = connection.execute(
            "SELECT COUNT(*) FROM attendance WHERE attendance_date = ?",
            (attendance_date,),
        ).fetchone()[0]
        attendance_total = connection.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
        unregistered = connection.execute("SELECT COUNT(*) FROM unregistered").fetchone()[0]
    return {
        "students": int(students),
        "attendance_today": int(attendance_today),
        "attendance_total": int(attendance_total),
        "unregistered": int(unregistered),
    }


def export_all_data(db_path: str | Path | None = None) -> dict[str, Any]:
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "exported_at": _now_parts()[0],
        "students": get_students(db_path),
        "attendance": get_attendance(limit=100_000, db_path=db_path),
        "unregistered": get_unregistered(db_path),
    }
