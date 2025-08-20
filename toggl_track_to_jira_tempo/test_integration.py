#!/usr/bin/env python3
"""
Integration test to verify the sync tracking works with the actual sync logic.
This test mocks the API calls to avoid making real requests.
"""

import os
import tempfile
import unittest.mock
from sync_tracker import SyncTracker


def test_integration():
    """Test the integration between sync logic and tracking."""
    print("Testing sync integration with tracking...")

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        test_db_path = tmp_file.name

    try:
        # Mock the APIs and config to avoid real API calls
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

            # Create a real tracker instance for the mock to use
            real_tracker = SyncTracker(test_db_path)
            MockSyncTracker.return_value = real_tracker

            # Mock Toggl API response with grouped entries
            mock_toggl = MockTogglAPI.return_value
            mock_toggl.get_time_entries.return_value = [
                {
                    "id": 1001,  # This will be the main ID for the grouped entry
                    "description": "TEST-123: Test work -- Working on tests",
                    "duration": 3600,
                    "start": "2025-01-15T09:00:00+00:00",
                    "original_toggl_ids": [1001, 1002, 1003]  # Multiple original IDs
                },
                {
                    "id": 2001,
                    "description": "TEST-456: Another task -- Different work",
                    "duration": 1800,
                    "start": "2025-01-15T14:00:00+00:00",
                    "original_toggl_ids": [2001]  # Single original ID
                }
            ]

            # Mock Jira API response
            mock_jira = MockJiraAPI.return_value
            mock_jira.get_issue_details.return_value = {
                "id": "12345",
                "fields": {"summary": "Test issue"}
            }

            # Mock Tempo API response
            mock_tempo = MockTempoAPI.return_value
            mock_tempo.add_worklog.return_value = {"tempoWorklogId": "tempo-123"}

            # Import and run the sync function
            from sync import sync

            print("✓ Running first sync...")

            # Mock the user interactions to always continue
            with unittest.mock.patch('builtins.input', return_value=''):
                with unittest.mock.patch('sync.Logger'):  # Suppress logging output
                    sync("2025-01-15", "2025-01-15")

            print("✓ First sync completed")

            # Verify that entries were tracked
            records = real_tracker.list_synced_entries()
            assert len(records) == 2, f"Expected 2 records, got {len(records)}"

            # Check first record (grouped entry)
            record1 = next(r for r in records if r['issue_key'] == 'TEST-123')
            assert record1['toggl_ids'] == [1001, 1002, 1003], "Should track all original IDs"
            assert record1['duration'] == 3600, "Should track correct duration"

            # Check second record (single entry)
            record2 = next(r for r in records if r['issue_key'] == 'TEST-456')
            assert record2['toggl_ids'] == [2001], "Should track single original ID"
            assert record2['duration'] == 1800, "Should track correct duration"

            print("✓ All entries were tracked correctly")

            # Reset the tempo API mock to verify no new calls are made
            mock_tempo.add_worklog.reset_mock()

            print("✓ Running second sync (should skip all entries)...")

            # Run sync again - should skip all entries
            with unittest.mock.patch('builtins.input', return_value=''):
                with unittest.mock.patch('sync.Logger'):  # Suppress logging output
                    sync("2025-01-15", "2025-01-15")

            # Verify no new worklog calls were made
            assert not mock_tempo.add_worklog.called, "No new worklogs should be created on second run"

            print("✓ Second sync correctly skipped all entries")

            # Verify no new records were added
            records_after = real_tracker.list_synced_entries()
            assert len(records_after) == 2, "Should still have exactly 2 records"

            print("✓ No duplicate records were created")

        print("\n🎉 Integration test passed! Sync tracking is working correctly with the sync logic.")

    finally:
        # Clean up test database
        if os.path.exists(test_db_path):
            os.unlink(test_db_path)
            print(f"✓ Cleaned up test database: {test_db_path}")


if __name__ == "__main__":
    test_integration()
