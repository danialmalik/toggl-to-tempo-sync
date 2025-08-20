#!/usr/bin/env python3
"""
Test script to verify the sync tracking system works correctly.
"""

import os
import tempfile
from sync_tracker import SyncTracker


def test_sync_tracker():
    """Test the sync tracker functionality."""
    print("Testing Sync Tracker...")

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        test_db_path = tmp_file.name

    try:
        tracker = SyncTracker(test_db_path)

        # Test data
        toggl_ids = [1001, 1002]
        issue_key = "TEST-123"
        description = "Test work entry"
        duration = 3600  # 1 hour
        start_date = "2025-01-15"

        print(f"✓ Created tracker with database: {test_db_path}")

        # Test 1: Entry should not be synced initially
        is_synced = tracker.is_entry_synced(toggl_ids, issue_key, description, duration, start_date)
        assert not is_synced, "Entry should not be synced initially"
        print("✓ Entry correctly identified as not synced")

        # Test 2: Record a sync
        entry_hash = tracker.record_sync(
            toggl_ids=toggl_ids,
            issue_key=issue_key,
            description=description,
            duration=duration,
            start_date=start_date,
            tempo_worklog_id="tempo-123",
            additional_data={"test": True}
        )
        print(f"✓ Recorded sync with hash: {entry_hash[:12]}...")

        # Test 3: Entry should now be synced
        is_synced = tracker.is_entry_synced(toggl_ids, issue_key, description, duration, start_date)
        assert is_synced, "Entry should be synced after recording"
        print("✓ Entry correctly identified as synced")

        # Test 4: Order independence (reversed IDs should still match)
        reversed_ids = [1002, 1001]
        is_synced_reversed = tracker.is_entry_synced(reversed_ids, issue_key, description, duration, start_date)
        assert is_synced_reversed, "Entry should be synced regardless of ID order"
        print("✓ Order independence working correctly")

        # Test 5: Different entry should not be synced
        is_different_synced = tracker.is_entry_synced(
            toggl_ids=[2001, 2002],
            issue_key="TEST-456",
            description="Different work",
            duration=1800,
            start_date="2025-01-16"
        )
        assert not is_different_synced, "Different entry should not be synced"
        print("✓ Different entry correctly identified as not synced")

        # Test 6: List records
        records = tracker.list_synced_entries()
        assert len(records) == 1, "Should have exactly one record"
        assert records[0]['issue_key'] == issue_key, "Record should match original data"
        print("✓ Record retrieval working correctly")

        # Test 7: Delete record
        deleted = tracker.delete_sync_record(entry_hash)
        assert deleted, "Record should be deleted successfully"
        print("✓ Record deletion working correctly")

        # Test 8: Entry should not be synced after deletion
        is_synced_after_delete = tracker.is_entry_synced(toggl_ids, issue_key, description, duration, start_date)
        assert not is_synced_after_delete, "Entry should not be synced after deletion"
        print("✓ Entry correctly identified as not synced after deletion")

        print("\n🎉 All tests passed! Sync tracker is working correctly.")

    finally:
        # Clean up test database
        if os.path.exists(test_db_path):
            os.unlink(test_db_path)
            print(f"✓ Cleaned up test database: {test_db_path}")


if __name__ == "__main__":
    test_sync_tracker()
