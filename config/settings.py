"""Environment-driven application settings.

Values are read from environment variables (optionally loaded from ``.env``)
and, when deployed on Streamlit Community Cloud, from ``st.secrets``.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _get(key: str, default: str) -> str:
    try:
        import streamlit as st

        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


def _get_bool(key: str, default: bool) -> bool:
    return _get(key, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _get_float(key: str, default: float) -> float:
    try:
        return float(_get(key, str(default)))
    except (TypeError, ValueError):
        return default


def _get_path(key: str, default: Path) -> Path:
    raw = Path(_get(key, str(default))).expanduser()
    return raw if raw.is_absolute() else BASE_DIR / raw


APP_NAME = _get("APP_NAME", "Smart Teaching Assistant")
APP_VERSION = _get("APP_VERSION", "0.1.0")
APP_TAGLINE = _get(
    "APP_TAGLINE",
    "Face-recognition attendance, student records and classroom insights in one place.",
)

DEMO_MODE = _get_bool("DEMO_MODE", True)
ATTENDANCE_THRESHOLD = _get_float("ATTENDANCE_THRESHOLD", 0.60)

DATA_DIR = _get_path("DATA_DIR", Path("data"))
FACES_DIR = _get_path("FACES_DIR", DATA_DIR / "faces")
DB_PATH = _get_path("DATABASE_PATH", DATA_DIR / "teaching_assistant.db")


def data_path(value: str | Path) -> Path:
    """Resolve a stored data path (relative paths are relative to ``DATA_DIR``)."""
    path = Path(value)
    return path if path.is_absolute() else DATA_DIR / path


def ensure_directories() -> None:
    """Create the local storage directories when missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FACES_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


ensure_directories()
