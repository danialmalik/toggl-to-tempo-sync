import os
import datetime
from typing import Optional

import requests
from jira_api import JiraAPI
from toggle_api import TogglTrackAPI
from jira_tempo_api import JiraTempoAPI
from sync_tracker import SyncTracker
from pprint import pprint
from config import config
from utils import Logger


TOGGL_TRACK_AUTH_TOKEN = config.toggl.api_key
JIRA_TEMPO_AUTH_TOKEN = config.tempo.api_key
JIRA_TEMPO_ACCOUNT_ID = config.tempo.user_id


def confirm(message: str):
    Logger.log_info(message)

    confirm_prompt = Logger.format_message("Confirm? [y/n]: ", Logger.INFO_SECONDARY)
    Logger.log_info_raw(confirm_prompt)
    return input(f"{message} [y/n]: ").lower().strip() == "y"

def input_choice(prompt: str, choices: list):
    Logger.log_info(prompt)
    for i, choice in enumerate(choices):
        choice_formatted = Logger.format_message(choice, Logger.INFO_SECONDARY)
        Logger.log_info(f"{i+1}. {choice_formatted}")

    choice = input(f"Enter choice [1-{len(choices)}]: ")
    try:
        return choices[int(choice)-1]
    except (ValueError, IndexError, KeyError):
        Logger.log_error("Invalid choice. Please try again.")
        return input_choice(prompt, choices)

def wait_for_enter(msg: str):
    formatted_msg = Logger.format_message(f"{msg}. Press enter to continue...", Logger.INFO_SECONDARY)
    input(formatted_msg)

def seconds_to_human_readable(seconds: int):
    return str(datetime.timedelta(seconds=seconds))

def input_or_default(prompt: str, default: str):
    default_formatted = Logger.format_message(default, Logger.INFO_SECONDARY)
    value = input(f"{prompt} [{default_formatted}]: ")
    return value or default

def sync(start_date: str, end_date: Optional[str] = None):
    toggl_api = TogglTrackAPI(auth_token=TOGGL_TRACK_AUTH_TOKEN)
    jira_tempo_api = JiraTempoAPI(account_id=JIRA_TEMPO_ACCOUNT_ID, auth_token=JIRA_TEMPO_AUTH_TOKEN)
    jira_api = JiraAPI(
        subdomain=config.jira.subdomain,
        user_email=config.jira.user_email,
        api_token=config.jira.api_token
    )

    # Initialize sync tracker
    sync_tracker = SyncTracker()

    entries = toggl_api.get_time_entries(
        start_date=start_date,
        end_date=end_date,
        group=True,
        round_seconds_to=60,
        # skip_entry_substr="SKIP",
        exclude_tags=["banked_hours", "unpaid", "skip_tempo"],
        exclude_projects=["Hours Bank"],

    )

    synced_count = 0
    skipped_count = 0
    total_entries = len(entries)

    Logger.log_info(f"Found {total_entries} entries to process...")

    for entry in entries:
        issue_key = entry["description"].split(":")[0]
        issue_description = "--" in entry["description"] and entry["description"].split("--")[1] or ""
        issue_description = issue_description.strip()
        duration = entry["duration"]
        datetime_obj = datetime.datetime.strptime(entry["start"], "%Y-%m-%dT%H:%M:%S+00:00")
        entry_date = datetime_obj.date()
        entry_date_str = str(entry_date)

        # Get original Toggl IDs (either from grouped entry or single entry)
        original_toggl_ids = entry.get("original_toggl_ids", [entry["id"]])

        # Check if this entry has already been synced
        if sync_tracker.is_entry_synced(
            toggl_ids=original_toggl_ids,
            issue_key=issue_key,
            description=issue_description,
            duration=duration,
            start_date=entry_date_str
        ):
            issue_key_formatted = Logger.format_message(issue_key, Logger.INFO_SECONDARY)
            duration_formatted = Logger.format_message(seconds_to_human_readable(duration), Logger.SUCCESS)
            date_formatted = Logger.format_message(entry_date_str, Logger.INFO_SECONDARY)
            Logger.log_warning(f"SKIPPED (already synced): {issue_key_formatted} with {duration_formatted} on {date_formatted}")
            skipped_count += 1
            continue

        while True:
            try:
                # Format log variables with appropriate colors
                issue_key_formatted = Logger.format_message(issue_key, Logger.INFO_SECONDARY)
                duration_formatted = Logger.format_message(seconds_to_human_readable(duration), Logger.SUCCESS)
                date_formatted = Logger.format_message(entry_date_str, Logger.INFO_SECONDARY)
                desc_formatted = Logger.format_message(f"\"{issue_description}\"", Logger.INFO_SECONDARY)

                # Get issue details including summary
                issue_details = jira_api.get_issue_details(issue_key)
                issue_id = issue_details["id"]
                issue_summary = issue_details.get("fields", {}).get("summary", "")
                summary_formatted = Logger.format_message(f"\"{issue_summary}\"", Logger.INFO_SECONDARY)

                Logger.log_info(f"Adding worklog for {issue_key_formatted} with {duration_formatted} on date {date_formatted}")
                Logger.log_info(f"Issue summary: {summary_formatted}")
                Logger.log_info(f"Description: {desc_formatted}")

                # Check if issue summary contains "Moved to" or "not in use" (case insensitive)
                if issue_summary and ("moved to" in issue_summary.lower() or "not in use" in issue_summary.lower()):
                    warning_text = Logger.format_message("WARNING: This issue appears to be deprecated or moved.", Logger.WARNING)
                    Logger.log_warning(warning_text)

                    options = ["Continue Anyway", "Modify Details", "Skip"]
                    choice = input_choice("Issue may be deprecated or moved. Choose an option:", options)

                    if choice == "Skip":
                        Logger.log_warning(f"Skipping worklog for {issue_key_formatted}...")
                        break
                    elif choice == "Modify Details":
                        issue_key = input_or_default("Issue key", issue_key)
                        duration = int(input_or_default("Time spent (seconds)", str(duration)))
                        entry_date_str = input_or_default("Start date (YYYY-MM-DD)", entry_date_str)
                        issue_description = input_or_default("Description", issue_description)
                        continue

                # Add worklog to Tempo
                worklog_result = jira_tempo_api.add_worklog(
                    issue_id=issue_id,
                    time_spent_seconds=duration,
                    start_date=entry_date_str,
                    description=issue_description
                )

                # Record successful sync
                tempo_worklog_id = worklog_result.get("tempoWorklogId") if isinstance(worklog_result, dict) else None
                sync_tracker.record_sync(
                    toggl_ids=original_toggl_ids,
                    issue_key=issue_key,
                    description=issue_description,
                    duration=duration,
                    start_date=entry_date_str,
                    tempo_worklog_id=tempo_worklog_id,
                    additional_data={
                        "issue_id": issue_id,
                        "issue_summary": issue_summary,
                        "sync_date_range": f"{start_date} to {end_date or start_date}"
                    }
                )

                Logger.log_success("Done...\n")
                synced_count += 1
                break

            except Exception as e:
                if isinstance(e, requests.exceptions.HTTPError):
                    error_message = e.response.text
                else:
                    error_message = str(e)

                issue_key_formatted = Logger.format_message(issue_key, Logger.INFO_SECONDARY)
                error_formatted = Logger.format_message(error_message, Logger.ERROR)
                Logger.log_error(f"Failed to add worklog for {issue_key_formatted}: {error_formatted}")

                options = ["Retry", "Skip", "Manual Entry", "Open JIRA Issue", "Exit"]
                choice = input_choice("Choose an option:", options)

                if choice == "Retry":
                    Logger.log_info(f"Retrying worklog for {issue_key_formatted}...", Logger.INFO_SECONDARY)
                    continue

                elif choice == "Skip":
                    Logger.log_warning(f"Skipping worklog for {issue_key_formatted}...")
                    break

                elif choice == "Exit":
                    exit(1)

                elif choice == "Manual Entry":
                    issue_key = input_or_default("Issue key", issue_key)
                    duration = int(input_or_default("Time spent (seconds)", str(duration)))
                    entry_date_str = input_or_default("Start date (YYYY-MM-DD)", entry_date_str)
                    issue_description = input_or_default("Description", issue_description)
                    continue

                elif choice == "Open JIRA Issue":
                    issue_key_stripped = issue_key.strip()
                    url = f"https://trader.atlassian.net/browse/{issue_key_stripped}"
                    jira_url_formatted = Logger.format_message(url, Logger.INFO)
                    issue_formatted = Logger.format_message(issue_key_stripped, Logger.INFO_SECONDARY)
                    Logger.log_info(f"Opening JIRA issue {issue_formatted} in browser: {jira_url_formatted}")
                    os.system(f"open {url}")

                    wait_for_enter("Waiting for confirmation before retrying...")
                    continue

    # Print summary
    Logger.log_info("=" * 50)
    Logger.log_info("SYNC SUMMARY")
    Logger.log_info("=" * 50)
    Logger.log_success(f"Successfully synced: {synced_count} entries")
    Logger.log_warning(f"Skipped (already synced): {skipped_count} entries")
    Logger.log_info(f"Total processed: {total_entries} entries")
    Logger.log_info("=" * 50)



def get_past_working_day() -> str:
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    while yesterday.weekday() in [5, 6]:
        yesterday -= datetime.timedelta(days=1)

    return yesterday.strftime("%Y-%m-%d")


def print_help():
    help_cmd = Logger.format_message("python cli.py sync [start_date] [end_date]", Logger.INFO_SECONDARY)
    Logger.log_info(f"Usage: {help_cmd}")
    Logger.log_info("start_date and end_date are optional. If not provided, the script will prompt for them.")


def main(*args):
    start_date, end_date = None, None

    if len(args) > 0 and args[0] == "help":
        print_help()
        return

    if len(args) > 0:
        start_date = args[0]

    if len(args) == 2:
        end_date = args[1]

    last_working_day = get_past_working_day()

    if not start_date:
        default_date = Logger.format_message(last_working_day, Logger.INFO_SECONDARY)
        start_date = input(f"Enter start date (yyyy-mm-dd) [{default_date}]: ") or last_working_day

    if not end_date:
        default_date = Logger.format_message(last_working_day, Logger.INFO_SECONDARY)
        end_date = input(f"Enter end date (yyyy-mm-dd) [{default_date}]: ") or last_working_day

    sync(start_date, end_date)
