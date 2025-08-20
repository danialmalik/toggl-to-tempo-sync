# Sync Tracking System

The toggl-to-tempo sync tool now includes a robust tracking system to prevent duplicate entries when re-running the sync process.

## How It Works

### Automatic Tracking
- Every successfully synced entry is recorded in a SQLite database (`sync_records.db`)
- Each entry is identified by a unique hash generated from:
  - Original Toggl entry IDs (sorted for consistency)
  - Issue key (e.g., "PROJ-123")
  - Description
  - Duration in seconds
  - Start date

### Grouped Entries Support
When entries are grouped (same description and date), the system:
- Preserves all original Toggl entry IDs in an `original_toggl_ids` field
- Sorts these IDs to ensure consistent hashing regardless of processing order
- Uses the combined set of IDs for tracking

### Duplicate Prevention
Before syncing each entry, the system:
1. Checks if the entry hash already exists in the tracking database
2. Skips the entry if already synced (shows "SKIPPED (already synced)" message)
3. Only processes entries that haven't been synced before

## Usage

### Regular Sync
```bash
python cli.py sync 2025-01-01 2025-01-31
```

The sync process will now show:
- Total entries found
- Entries skipped (already synced)
- Entries successfully synced
- Summary at the end

### Managing Sync Records

#### List all sync records
```bash
python cli.py sync-records list
```

#### List records for a specific date range
```bash
python cli.py sync-records list --start-date 2025-01-01 --end-date 2025-01-31
```

#### Show statistics
```bash
python cli.py sync-records stats
```

#### Use a custom database path
```bash
python cli.py sync-records --db-path custom.db list
```

#### Delete a specific record (to allow re-syncing)
```bash
python cli.py sync-records delete <entry_hash>
```

#### Clear all records (use with caution)
```bash
python cli.py sync-records clear --confirm
```

## Database Schema

The tracking database stores:
- `entry_hash`: Unique identifier for the entry
- `toggl_ids`: JSON array of original Toggl entry IDs
- `issue_key`: JIRA issue key
- `description`: Entry description
- `duration`: Duration in seconds
- `start_date`: Entry date
- `tempo_worklog_id`: Tempo worklog ID (if available)
- `sync_timestamp`: When the sync was performed
- `additional_data`: Extra metadata (issue summary, sync date range, etc.)

## Benefits

1. **Reliability**: Re-run sync processes without fear of duplicates
2. **Visibility**: Track what has been synced and when
3. **Debugging**: Identify problematic entries or patterns
4. **Recovery**: Delete specific records to allow re-syncing if needed
5. **Analytics**: View statistics about your time tracking patterns

## File Location

The sync records database is stored as `sync_records.db` in the same directory as your scripts. This file is automatically created on first use and can be safely backed up or moved if needed.

## Migration

This feature is backward compatible. Existing workflows will continue to work, but entries synced before this update won't be tracked. The tracking will begin from the first sync run after implementing this feature.
