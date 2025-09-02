#!/usr/bin/env python3
"""
Test the complete animated sync integration with mocked APIs.
"""

import unittest.mock
import tempfile
import os
from sync_tracker import SyncTracker


def test_animated_sync_integration():
    """Test the animated sync with mock APIs."""
    print("🧪 Testing animated sync integration...")

    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        test_db_path = tmp_file.name

    try:
        # Mock the APIs and config
        with unittest.mock.patch('sync.config') as mock_config, \
             unittest.mock.patch('sync.TogglTrackAPI') as MockTogglAPI, \
             unittest.mock.patch('sync.JiraTempoAPI') as MockTempoAPI, \
             unittest.mock.patch('sync.JiraAPI') as MockJiraAPI, \
             unittest.mock.patch('sync.SyncTracker') as MockSyncTracker:

            # Configure mocks
            mock_config.toggl.api_key = "test_key"
            mock_config.tempo.api_key = "test_key"
            mock_config.tempo.user_id = "test_user"
            mock_config.jira.subdomain = "test"
            mock_config.jira.user_email = "test@example.com"
            mock_config.jira.api_token = "test_token"

            # Create real tracker for testing
            real_tracker = SyncTracker(test_db_path)
            MockSyncTracker.return_value = real_tracker

            # Mock Toggl API - one entry that will be synced, one already synced
            mock_toggl = MockTogglAPI.return_value
            mock_toggl.get_time_entries.return_value = [
                {
                    "id": 1001,
                    "description": "NEW-123: New work -- Fresh task",
                    "duration": 3600,
                    "start": "2025-08-25T09:00:00+00:00",
                    "original_toggl_ids": [1001]
                },
                {
                    "id": 1002,
                    "description": "OLD-456: Old work -- Already synced",
                    "duration": 1800,
                    "start": "2025-08-25T14:00:00+00:00",
                    "original_toggl_ids": [1002]
                }
            ]

            # Pre-sync one entry to test skip behavior
            real_tracker.record_sync([1002], 'OLD-456', 'Already synced', 1800, '2025-08-25')

            # Mock JIRA API
            mock_jira = MockJiraAPI.return_value
            mock_jira.get_issue_details.return_value = {
                "id": "12345",
                "fields": {"summary": "Test issue"}
            }

            # Mock Tempo API
            mock_tempo = MockTempoAPI.return_value
            mock_tempo.add_worklog.return_value = {"tempoWorklogId": "tempo-123"}

            # Import and run sync with mocked input
            from sync import sync

            print("🚀 Running animated sync demo...")

            # Mock user input to avoid prompts
            with unittest.mock.patch('builtins.input', return_value=''):
                sync("2025-08-25", "2025-08-25")

            print("✅ Animated sync completed successfully!")

            # Verify tracking worked
            records = real_tracker.list_synced_entries()
            print(f"📊 Total records in database: {len(records)}")

            # Should have 2 records now (1 pre-existing + 1 newly synced)
            assert len(records) == 2, f"Expected 2 records, got {len(records)}"
            print("✅ Tracking verification passed!")

    finally:
        # Clean up
        if os.path.exists(test_db_path):
            os.unlink(test_db_path)
            print(f"🧹 Cleaned up test database")


if __name__ == "__main__":
    test_animated_sync_integration()
