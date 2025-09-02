# Automation scripts for Toggl Track <-> JIRA Tempo

## Description

This repository contains scripts to automate the process of creating  Tempo worklogs in JIRA based on Toggl time entries.

### Guidelines

**Important**: Time entries added in Toggl Track must be in this pattern:

`<JIRA_ISSUE_KEY>: <GENERAL_DESCRIPTION> -- <DESCRIPTION_FOR_TEMPO>`

- `<JIRA_ISSUE_KEY>`: JIRA issue key for which the worklog is to be created.
- `<GENERAL_DESCRIPTION>`: General description of the work done. This is just for your reference. This part will not be sent to JIRA.
- `<DESCRIPTION_FOR_TEMPO>`: Description for the worklog entry in JIRA Tempo.

Example:

`ABC-123: Frontend bug fix task -- Worked on fixing the bug `


## Usage

```sh
# Prints available commands and instructions
python cli.py
```

```sh
# Prints help for a given command
python cli.py <command> help
```

### Configuration

- Prepare the `config.json` file.

```sh
cp toggle_track_to_jira_tempo/config.json.example toggle_track_to_jira_tempo/config.json
```

- Fill in the required fields in the `config.json` file.
- Read https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located to get the Toggl API key.
- To get **tempo user ID**:
  - Open your JIRA dashboard.
  - Click on your profile icon on the top right corner.
  - Click on the "Profile" option.
  - The URL will be something like `https://trader.atlassian.net/jira/people/<YOUR_ID>`.
  - Copy the `<YOUR_ID>` part and paste it in the `config.json` file.

### Commands

- `sync`: Sync Toggl time entries to JIRA Tempo worklogs

```sh
python cli.py sync help
```

- `get-summary`: Get summary of tempo time entries

```sh
python cli.py get-summary help
```

- `sync-records`: Manage sync tracking records (new!)

```sh
# List all synced entries
python cli.py sync-records list

# Show sync statistics
python cli.py sync-records stats

# List entries for a specific date range
python cli.py sync-records list --start-date 2025-01-01 --end-date 2025-01-31

# Use a custom database path
python cli.py sync-records --db-path custom.db list

# Delete a specific sync record (to allow re-syncing)
python cli.py sync-records delete <entry_hash>

# Clear all sync records (use with caution)
python cli.py sync-records clear --confirm
```## New Feature: Duplicate Prevention

The sync tool now automatically tracks synced entries to prevent duplicates when re-running the sync process. Key features:

- **Automatic tracking**: Every successful sync is recorded in a local SQLite database
- **Smart duplicate detection**: Handles grouped entries and order-independent ID matching
- **Resume capability**: Re-run sync commands safely - already synced entries will be skipped
- **Management tools**: View, delete, and manage sync records as needed

## New Feature: Enhanced UI with Animated Progress

The sync tool now features a beautiful, modern terminal interface with:

- **🎯 Animated spinners**: Visual feedback during API calls (fetching, validating, syncing)
- **📊 Progress tracking**: Clear progress indicators showing [current/total] entries
- **🎨 Rich status display**: Emoji-based status indicators for success ✅, skip ⏭️, and failure ❌
- **📋 Enhanced summaries**: Detailed sync statistics with success rates and visual formatting
- **⚡ Real-time updates**: Live progress updates as entries are processed

The new interface makes it easy to:
- Track sync progress in real-time
- Identify issues immediately with clear error indicators
- See detailed statistics at completion
- Understand what happened with each entry

See [SYNC_TRACKING.md](SYNC_TRACKING.md) for detailed documentation.

### Benefits
- ✅ No more duplicate worklogs when re-running sync
- ✅ Clear visibility into what has been synced
- ✅ Beautiful, professional terminal interface
- ✅ Real-time progress feedback
- ✅ Ability to track and analyze your time entry patterns
- ✅ Safe recovery options if you need to re-sync specific entries


## Tips

- You can make a bash alias to run the script easily.

```sh
alias sync-logs="python <PATH_TO_CLI_FOLDER>/cli.py"
```

And then use this as:

```sh
# Sync yesterday's time entries
sync-logs sync

# Get summary of tempo time entries
sync-logs get-summary
```
