# Automation scripts for Toggle <-> JIRA Tempo

## Description

This repository contains scripts to automate the process of creating  Tempo worklogs in JIRA based on Toggl time entries.

### Guidelines

**Important**: Time entries added in Toggl Track must be in this pattern:

`<JIRA_ISSUE_KEY>: <GENERAL_DESCRIPTION> -- <DESCRIPTION_FOR_TEMPO>`

- `<JIRA_ISSUE_KEY>`: JIRA issue key for which the worklog is to be created.
- `<GENERAL_DESCRIPTION>`: General description of the work done. This is just for your reference. This part will not be sent to JIRA.
- `<DESCRIPTION_FOR_TEMPO>`: Description for the worklog entry in JIRA Tempo.

Example:

`ABC-123: Frontend big fix task -- Worked on fixing the bug `


## Usage

```sh

# Gives available commands and instructions
python cli.py
```

```sh
# Get help for a given command
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
