"""Defaults for CLI args"""
import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SYNC_DB_PATH = os.path.join(_CURRENT_DIR, "sync_records.db")


__all__ = [
    "DEFAULT_SYNC_DB_PATH",
]
