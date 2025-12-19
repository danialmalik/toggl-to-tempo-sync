import sqlite3
import os
import json
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime

from cli_defaults import DEFAULT_SYNC_DB_PATH


class SyncTracker:
    """
    Tracks synced Toggl entries to prevent duplicates when re-running sync.
    Uses SQLite database to store sync records.
    """

    def __init__(self, db_path: str = DEFAULT_SYNC_DB_PATH):
        """Initialize the sync tracker with database path."""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the SQLite database and create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sync_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_hash TEXT UNIQUE NOT NULL,
                    toggl_ids TEXT NOT NULL,  -- JSON array of original Toggl entry IDs
                    issue_key TEXT NOT NULL,
                    description TEXT,
                    duration INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    tempo_worklog_id TEXT,  -- If Tempo returns a worklog ID
                    sync_timestamp TEXT NOT NULL,
                    additional_data TEXT  -- JSON for any extra metadata
                )
            """)

            # Create an index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_entry_hash
                ON sync_records(entry_hash)
            """)

            # Create an index for toggl_ids lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_toggl_ids
                ON sync_records(toggl_ids)
            """)

            conn.commit()

    def _generate_entry_hash(self, toggl_ids: List[int], issue_key: str,
                           description: str, duration: int, start_date: str) -> str:
        """
        Generate a unique hash for an entry based on its key characteristics.
        Uses sorted toggl_ids to ensure order independence.
        """
        # Sort IDs to ensure consistent hash regardless of order
        sorted_ids = sorted(toggl_ids)

        # Create a string representation of the key data
        key_data = f"{sorted_ids}|{issue_key}|{description}|{duration}|{start_date}"

        # Generate SHA256 hash
        return hashlib.sha256(key_data.encode('utf-8')).hexdigest()

    def is_entry_synced(self, toggl_ids: List[int], issue_key: str,
                       description: str, duration: int, start_date: str) -> bool:
        """
        Check if an entry has already been synced.

        Args:
            toggl_ids: List of original Toggl entry IDs that make up this entry
            issue_key: JIRA issue key
            description: Entry description
            duration: Duration in seconds
            start_date: Start date string (YYYY-MM-DD format)

        Returns:
            True if already synced, False otherwise
        """
        entry_hash = self._generate_entry_hash(toggl_ids, issue_key, description, duration, start_date)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM sync_records WHERE entry_hash = ?
            """, (entry_hash,))

            count = cursor.fetchone()[0]
            return count > 0

    def record_sync(self, toggl_ids: List[int], issue_key: str,
                   description: str, duration: int, start_date: str,
                   tempo_worklog_id: Optional[str] = None,
                   additional_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Record a successful sync to prevent future duplicates.

        Args:
            toggl_ids: List of original Toggl entry IDs that make up this entry
            issue_key: JIRA issue key
            description: Entry description
            duration: Duration in seconds
            start_date: Start date string (YYYY-MM-DD format)
            tempo_worklog_id: Tempo worklog ID if available
            additional_data: Any additional metadata to store

        Returns:
            The entry hash for reference
        """
        entry_hash = self._generate_entry_hash(toggl_ids, issue_key, description, duration, start_date)
        sync_timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Convert lists/dicts to JSON for storage
            toggl_ids_json = json.dumps(sorted(toggl_ids))
            additional_data_json = json.dumps(additional_data) if additional_data else None

            try:
                cursor.execute("""
                    INSERT INTO sync_records
                    (entry_hash, toggl_ids, issue_key, description, duration,
                     start_date, tempo_worklog_id, sync_timestamp, additional_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (entry_hash, toggl_ids_json, issue_key, description, duration,
                      start_date, tempo_worklog_id, sync_timestamp, additional_data_json))

                conn.commit()
                return entry_hash

            except sqlite3.IntegrityError:
                # Entry already exists, which is fine
                return entry_hash

    def get_sync_record(self, entry_hash: str) -> Optional[Dict[str, Any]]:
        """Get sync record details by hash."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT entry_hash, toggl_ids, issue_key, description, duration,
                       start_date, tempo_worklog_id, sync_timestamp, additional_data
                FROM sync_records WHERE entry_hash = ?
            """, (entry_hash,))

            row = cursor.fetchone()
            if row:
                return {
                    'entry_hash': row[0],
                    'toggl_ids': json.loads(row[1]),
                    'issue_key': row[2],
                    'description': row[3],
                    'duration': row[4],
                    'start_date': row[5],
                    'tempo_worklog_id': row[6],
                    'sync_timestamp': row[7],
                    'additional_data': json.loads(row[8]) if row[8] else None
                }
        return None

    def list_synced_entries(self, start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all synced entries, optionally filtered by date range.

        Args:
            start_date: Filter entries from this date (YYYY-MM-DD)
            end_date: Filter entries to this date (YYYY-MM-DD)

        Returns:
            List of sync record dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = """
                SELECT entry_hash, toggl_ids, issue_key, description, duration,
                       start_date, tempo_worklog_id, sync_timestamp, additional_data
                FROM sync_records
            """
            params = []

            if start_date or end_date:
                conditions = []
                if start_date:
                    conditions.append("start_date >= ?")
                    params.append(start_date)
                if end_date:
                    conditions.append("start_date <= ?")
                    params.append(end_date)
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY start_date, sync_timestamp"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [
                {
                    'entry_hash': row[0],
                    'toggl_ids': json.loads(row[1]),
                    'issue_key': row[2],
                    'description': row[3],
                    'duration': row[4],
                    'start_date': row[5],
                    'tempo_worklog_id': row[6],
                    'sync_timestamp': row[7],
                    'additional_data': json.loads(row[8]) if row[8] else None
                }
                for row in rows
            ]

    def delete_sync_record(self, entry_hash: str) -> bool:
        """
        Delete a sync record (useful if you need to re-sync an entry).

        Args:
            entry_hash: The hash of the entry to delete

        Returns:
            True if record was deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sync_records WHERE entry_hash = ?", (entry_hash,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_records(self) -> int:
        """
        Clear all sync records (use with caution).

        Returns:
            Number of records deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sync_records")
            count = cursor.rowcount
            conn.commit()
            return count
